"""Public task formula; SciPy quadrature and independent transformed quadrature."""
import json
import math
import platform
from pathlib import Path
import scipy
from scipy.integrate import quad
from scipy.special import expit

ROOT = Path(__file__).resolve().parents[1]
NORMAL = math.gamma(1.5)

def integral(eta, tail, tolerance=2e-11):
    # expit avoids overflow in the Fermi occupation probability.
    upper, error = quad(lambda e: math.sqrt(e)*expit(eta-e), tail, math.inf,
                        epsabs=tolerance, epsrel=tolerance, limit=300)
    lower = 0.0
    if tail:
        lower, err = quad(lambda e: math.sqrt(tail)*math.exp((e-tail)/(2*tail))*expit(eta-e),
                          -math.inf, tail, epsabs=tolerance, epsrel=tolerance, limit=300)
        error += err
    return (lower+upper)/NORMAL, error/NORMAL

def independent(eta, tail):
    # Lower: u=exp((e-tail)/(2t)); upper: e=t+x^2 removes sqrt endpoint.
    lower = 0.0
    if tail:
        lower = 2*tail**1.5*quad(lambda u: expit(eta-tail-2*tail*math.log(u)),
                                0, 1, epsabs=2e-12, epsrel=2e-12, limit=300)[0]
    upper = quad(lambda x: 2*x*math.sqrt(tail+x*x)*expit(eta-tail-x*x),
                 0, math.inf, epsabs=2e-12, epsrel=2e-12, limit=300)[0]
    return (lower+upper)/NORMAL

def main():
    rows, errors, differences = [], [], []
    for tail in (0, 1, 10):
        for i in range(17):
            eta = -4+i/2
            value, error = integral(eta, tail)
            other = independent(eta, tail)
            assert math.isfinite(value) and value > 0
            assert abs(value-other) < 2e-9*max(1, abs(value))
            rows.append(dict(eta=eta, epsilon_t=tail, F=value))
            errors.append(error)
            differences.append(abs(value-other))
    lookup = {(r['eta'], r['epsilon_t']):r['F'] for r in rows}
    for tail in (0,1,10):
        assert all(lookup[(-4+i/2,tail)] < lookup[(-4+(i+1)/2,tail)] for i in range(16))
    for i in range(17):
        eta=-4+i/2
        assert lookup[(eta,0)] < lookup[(eta,1)] < lookup[(eta,10)]
    # Analytic no-tail anchor: (1 - 2^(-1/2))*zeta(3/2).
    from scipy.special import zeta
    anchor=(1-2**(-0.5))*zeta(1.5,1)
    assert abs(lookup[(0,0)]-anchor)<1e-11
    path=ROOT/'outputs/fermi_integral_values.json'
    text=json.dumps(rows, indent=2, allow_nan=False)+'\n'
    path.write_text(text, encoding='utf-8')
    loaded=json.loads(path.read_text())
    assert len(loaded)==51 and len({(r['eta'],r['epsilon_t']) for r in loaded})==51
    assert all(set(r)=={'eta','epsilon_t','F'} for r in loaded)
    report=dict(python=platform.python_version(),scipy=scipy.__version__, grid_points=51,
                maximum_quadrature_error_estimate=max(errors),
                maximum_independent_absolute_difference=max(differences),
                no_tail_zero_eta=lookup[(0,0)],large_tail_zero_eta=lookup[(0,10)],
                ratio_at_zero_eta=lookup[(0,10)]/lookup[(0,0)],
                monotonic_checks=True,analytic_anchor_passed=True,
                scientific_scope='Numerical validation of the supplied model, not experimental validation or platform score')
    (ROOT/'logs/validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
