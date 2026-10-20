"""Independent global optimization; does not import the task solver."""
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import expit

WORK = Path(__file__).resolve().parents[1]
X = np.array([9.4, 18.9, 27.5, 35.0])
Y = np.array([94.7, 85.3, 62.9, 39.0])


def predictions(p):
    return 100 * expit(-p[1] * (np.log(X) - p[0]))


def objective(p):
    return float(np.sum((predictions(p) - Y) ** 2))


def main():
    runs = []
    for seed in [491, 17, 303]:
        global_fit = differential_evolution(objective, [(np.log(1.), np.log(100.)), (.1, 20.)],
                                            seed=seed, tol=1e-12, maxiter=1000, polish=False)
        result = minimize(objective, global_fit.x, method='Nelder-Mead',
                          options={'xatol': 1e-13, 'fatol': 1e-12, 'maxiter': 5000})
        assert global_fit.success and result.success
        runs.append({'seed': seed, 'log_d0': float(result.x[0]), 'n': float(result.x[1]), 'sse': float(result.fun)})
    best = min(runs, key=lambda r: r['sse'])
    b, n = best['log_d0'], best['n']
    reference = {'a': float(np.exp(-n * b)), 'n': n, 'd0_nm': float(np.exp(b))}
    submitted = json.loads((WORK / 'outputs/fitted_params.json').read_text(encoding='utf-8'))
    assert set(submitted) == set(reference)
    for key, value in reference.items():
        assert np.isclose(submitted[key], value, rtol=2e-6, atol=1e-10), (key, submitted[key], value)
    rows = list(csv.DictReader((WORK / 'outputs/predicted_quenching.csv').open(encoding='utf-8', newline='')))
    assert len(rows) == 4
    distances = np.array([float(r['distance_nm']) for r in rows])
    values = np.array([float(r['predicted_quenching_pct']) for r in rows])
    assert np.array_equal(distances, X)
    recalculated = 100 / (1 + submitted['a'] * X ** submitted['n'])
    assert np.allclose(values, recalculated, rtol=0, atol=1e-10)
    output_sse = float(np.sum((values - Y)**2))
    assert abs(output_sse - best['sse']) < 1e-8
    report = {'checked_at': datetime.now(timezone.utc).isoformat(),
              'method': 'three seeded differential-evolution searches, polished independently with Nelder-Mead',
              'objective': 'unweighted SSE in original percentage-point units',
              'bounds': {'d0_nm': [1, 100], 'n': [.1, 20]},
              'reference': reference, 'submitted': submitted, 'searches': runs,
              'sse': output_sse, 'rmse_percentage_points': float(np.sqrt(output_sse / 4)),
              'csv_recomputation_max_error': float(np.max(np.abs(values-recalculated))),
              'passed': True, 'platform_score': None}
    (WORK / 'logs/host-independent-check.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
