"""Capture real subprocess command, exit code, stdout/stderr; rerun and verify."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'outputs').iterdir()) if p.is_file()}


def main():
    (ROOT/'logs').mkdir(parents=True, exist_ok=True)
    evidence = []
    initial = None
    for label, script in [('solve_first','solve.py'), ('solve_rerun','solve.py'), ('verify','verify.py')]:
        cmd = [sys.executable, str(ROOT/'scripts'/script)]
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        (ROOT/'logs'/f'{label}.stdout.log').write_text(result.stdout, encoding='utf-8')
        (ROOT/'logs'/f'{label}.stderr.log').write_text(result.stderr, encoding='utf-8')
        record = dict(label=label,command=cmd,cwd=str(ROOT),start_utc=start,exit_code=result.returncode)
        evidence.append(record)
        (ROOT/'logs/commands.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(record))
        if result.returncode:
            print(result.stderr)
            raise SystemExit(result.returncode)
        if label == 'solve_first':
            initial = hashes()
        elif label == 'solve_rerun':
            final = hashes()
            assert initial == final, 'Rerun outputs changed'
            (ROOT/'logs/reproducibility.json').write_text(json.dumps({'identical':True,'first':initial,'rerun':final},indent=2)+'\n',encoding='utf-8')
    print('Solver rerun identical; independent verification passed.')


if __name__ == '__main__':
    main()
