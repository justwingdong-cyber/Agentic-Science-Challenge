"""Focused checks for task boundaries and the output gate; no model calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('asc_agent', Path(__file__).with_name('asc_agent.py'))
agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)


class AgentChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)
        (self.work / 'outputs').mkdir()
        (self.work / 'result_summary.md').write_text('Independent checks are recorded here.')
        self.contract = {'outputs': [{'file': 'answer.json', 'format': 'json',
                                    'schema': {'required': {'value': 'float'}}}]}

    def tearDown(self):
        self.temp.cleanup()

    def answer(self, content):
        (self.work / 'outputs/answer.json').write_text(content)

    def test_reject_escape(self):
        for path in ('../secret', '/private', 'C:/secret', '..\\secret'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                agent.output_path(self.work, path)

    def test_reject_extra_files(self):
        self.answer('{"value": 1.0}')
        (self.work / 'outputs/cache.txt').write_text('unrelated')
        with self.assertRaisesRegex(ValueError, 'Unexpected files'):
            agent.validate(self.work, self.contract)

    def test_reject_wrong_number(self):
        for value in ('true', '"1.0"', 'NaN', 'null'):
            self.answer('{"value": ' + value + '}')
            with self.subTest(value=value), self.assertRaises(ValueError):
                agent.validate(self.work, self.contract)

    def test_credential_rejection(self):
        self.answer(json.dumps({'value': 1.0, 'note': 'asp_' + 'x' * 20}))
        with self.assertRaisesRegex(ValueError, 'credential'):
            agent.validate(self.work, self.contract)

    def test_valid_contract_is_not_scientific_verdict(self):
        self.answer('{"value": 1.0}')
        result = agent.validate(self.work, self.contract)
        self.assertTrue(result['contract_valid'])
        self.assertEqual(result['scientific_correctness'], 'requires task-specific verification')

    def test_read_only_public_statement_and_metadata(self):
        task = self.work / 'task'
        task.mkdir()
        (task / 'task.md').write_text('```json\n' + json.dumps(self.contract) + '\n```')
        # These disallowed files must not be opened or parsed.
        (task / 'checker.py').write_bytes(b'\xff\xfe')
        (task / 'solution.json').write_text('not JSON')
        (task / 'hidden_tests').mkdir()
        statement, metadata, contract, path = agent.read_task(self.work)
        self.assertEqual(path.name, 'task.md')
        self.assertEqual(contract, self.contract)
        self.assertEqual(metadata, {})


if __name__ == '__main__':
    unittest.main()
