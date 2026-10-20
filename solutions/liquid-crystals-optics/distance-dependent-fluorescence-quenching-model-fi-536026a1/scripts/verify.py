"""Independent formula, parameterization and optimizer; no solver imports."""
import csv
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, minimize_scalar

ROOT = Path(__file__).resolve().parents[1]


def main():
    out = ROOT/'outputs'
    assert {p.name for p in out.iterdir()} == {'fitted_params.json', 'predicted_quenching.csv'}
    params = json.loads((out/'fitted_params.json').read_text(encoding='utf-8'))
    assert set(params) == {'a', 'n', 'd0_nm'}
    assert all(type(v) is float and math.isfinite(v) and v > 0 for v in params.values())
    a, n, d0 = (params[k] for k in ['a', 'n', 'd0_nm'])
    with (out/'predicted_quenching.csv').open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['distance_nm', 'predicted_quenching_pct']
        rows = list(reader)
    x = [9.4, 18.9, 27.5, 35.0]
    y = [94.7, 85.3, 62.9, 39.0]
    assert len(rows) == 4
    predictions = [float(row['predicted_quenching_pct']) for row in rows]
    for i, row in enumerate(rows):
        assert float(row['distance_nm']) == x[i]
        assert math.isclose(predictions[i], 100/(1+a*x[i]**n), rel_tol=1e-12, abs_tol=1e-12)
    assert all(0 < q < 100 for q in predictions)
    assert all(predictions[i] > predictions[i+1] for i in range(3))
    assert math.isclose(d0, a**(-1/n), rel_tol=1e-12)
    assert math.isclose(100/(1+a*d0**n), 50, abs_tol=1e-10)
    # Independent scaled amplitude b=a*25**n; avoid small a and use scalar math.
    def objective(p):
        log_b, exponent = p
        if abs(log_b) > 200 or not 0 < exponent < 100:
            return 1e100
        b = math.exp(log_b)
        return sum((100/(1+b*(d/25)**exponent)-obs)**2 for d, obs in zip(x,y))
    independent = []
    for start in [(-1., 2.), (0., 4.), (1., 6.), (-2., 10.)]:
        opt = minimize(objective, start, method='Nelder-Mead',
                       options={'xatol': 1e-11, 'fatol': 1e-12, 'maxiter': 10000})
        assert opt.success
        independent.append(opt)
    best = min(independent, key=lambda r: r.fun)
    own_sse = sum((pred-obs)**2 for pred, obs in zip(predictions,y))
    independent_n = float(best.x[1])
    independent_d0 = 25*math.exp(-float(best.x[0])/independent_n)
    assert abs(own_sse-best.fun) < 1e-8
    assert abs(n-independent_n) < 1e-6
    assert abs(d0-independent_d0) < 1e-6
    # Central finite differences of independent SSE in (log_b,n).
    p = np.array([math.log(a)+n*math.log(25), n])
    h = 1e-4
    e = np.eye(2)*h
    gradient = np.array([(objective(p+v)-objective(p-v))/(2*h) for v in e])
    H = np.empty((2,2))
    for i in range(2):
        H[i,i] = (objective(p+e[i])-2*objective(p)+objective(p-e[i]))/h**2
    H[0,1] = H[1,0] = (objective(p+e[0]+e[1])-objective(p+e[0]-e[1])-objective(p-e[0]+e[1])+objective(p-e[0]-e[1]))/(4*h*h)
    eigenvalues = np.linalg.eigvalsh(H)
    assert max(abs(gradient)) < 1e-4
    assert min(eigenvalues) > 0
    fixed = {}
    for exponent in [4.,6.]:
        opt = minimize_scalar(lambda log_b: objective([log_b,exponent]), bounds=(-10,10), method='bounded', options={'xatol':1e-12})
        assert opt.success
        fixed[str(exponent)] = {'sse':float(opt.fun), 'd0_nm':25*math.exp(-opt.x/exponent)}
        assert opt.fun > own_sse
    report = {'passed':True, 'sse':own_sse, 'independent_n':independent_n,
              'independent_d0_nm':independent_d0, 'independent_sse':float(best.fun),
              'all_independent_sse':[float(r.fun) for r in independent],
              'finite_difference_gradient':gradient.tolist(), 'hessian_eigenvalues':eigenvalues.tolist(),
              'fixed_exponent_fits':fixed,
              'checks':['exact output set and schemas','four direct predictions','positive parameters',
                        'decreasing 0<Q<100','Q(d0)=50','independent optimization','stationary local minimum'],
              'limits':'Local checks, not platform scoring. Multistart is not a proof of global optimality.'}
    (ROOT/'logs/verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
