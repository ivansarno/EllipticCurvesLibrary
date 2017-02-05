import ECL
import random


def test_koblitz() -> bool:
    n = random.randrange(20000)
    point, padding = ECL.koblitz.iterative_encode(n, ECL.std_curves.CurveP192())
    return ECL.koblitz.decode(point, padding) == n and point.check(ECL.std_curves.CurveP192())