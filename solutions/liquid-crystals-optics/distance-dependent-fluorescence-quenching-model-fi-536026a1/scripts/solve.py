"""Fit the four public observations on the original percentage scale."""
from pathlib import Path
import csv
import json
import platform
import numpy as np
import scipy
from scipy.optimize import least_squares
from scipy.special import expit

ROOT = Path(__file__).resolve().parents[1]
X = np.array([9.4, 18.9, 27.5, 35.0])
Y = np.array([94.7, 85.3, 62.9, 39.0])


def residual(p):
    return 100 * expit(-p[1] * (np.log(X) - p[0])) - Y


def jacobian(p):
    q = expit(-p[1] * (np.log(X) - p[0]))
    factor = 100 * q * (1 - q)
    return np.column_stack((factor * p[1], -factor * (np.log(X) - p[0])))


def main():
    runs = []
    for d0 in [10., 25., 40., 80.]:
        for n in [1., 4., 6., 10.]:
            fit = least_squares(residual, [np.log(d0), n], jac=jacobian,
                                bounds=([-np.inf, 1e-8], [np.inf, np.inf]),
                                ftol=1e-13, xtol=1e-13, gtol=1e-12,
                                max_nfev=10000)
            if not fit.success:
                raise RuntimeError(fit.message)
            runs.append(fit)
    best = min(runs, key=lambda r: np.dot(r.fun, r.fun))
    log_d0, n = map(float, best.x)
    a = float(np.exp(-n * log_d0))
    d0 = float(a ** (-1 / n))
    params = dict(a=a, n=n, d0_nm=d0)
    predictions = 100 / (1 + a * X ** n)
    output = ROOT / 'outputs'
    output.mkdir(exist_ok=True)
    (output / 'fitted_params.json').write_text(json.dumps(params, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    with (output / 'predicted_quenching.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['distance_nm', 'predicted_quenching_pct'])
        writer.writerows(zip(X.tolist(), predictions.tolist()))
    report = dict(environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
                  parameters=params, predictions=predictions.tolist(),
                  residual_pred_minus_observed=(predictions-Y).tolist(),
                  sse=float(np.sum((predictions-Y)**2)),
                  rmse_percentage_points=float(np.sqrt(np.mean((predictions-Y)**2))),
                  gradient_in_logd0_n=(2*best.jac.T@best.fun).tolist(),
                  starts=[dict(p=r.x.tolist(), sse=float(r.fun@r.fun), nfev=r.nfev, message=r.message) for r in runs])
    (ROOT/'logs/fit_diagnostics.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
