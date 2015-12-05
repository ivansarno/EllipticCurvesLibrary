import random
import ECL
from ECL import *
from ECL import PointWOrder

__author__ = 'ivansarno'
__version__ = 'V.4.2'
__doc__ = """Test for package's feature"""


def test(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192, size=192):
    try:
        test_arithmetic(curve, point)
        test_diffie_hellman(point, size)
        test_el_gamal_koblitz(curve, point, size)
        test_representation(curve, point)
    except ECL.EclException:
        print("test ERROR: EclException Raised")
    except Exception:
        print("test ERROR: Other Exception Raised")


def test_diffie_hellman(point=ECL.std_curves.PointP192, size=192):
    user1 = ECL.DiffieHellman(point(), size)
    user2 = ECL.DiffieHellman(point(), size)
    message1 = user1.step1()
    message2 = user2.step1()
    user2.step2(message1)
    user1.step2(message2)
    if user1.key == user2.key:
        print("test diffie-hellman OK")
    else:
        print("test diffie-hellman ERROR")


def test_el_gamal_koblitz(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192, size=192):
    key = ECL.elgamal.keygen(point(), size)
    message = random.randint(0, 65535)
    m = ECL.koblitz.iterative_encode(message, curve())
    cipher = ECL.elgamal.encrypt(m[0], key[1], point())
    d = ECL.elgamal.decrypt(cipher[0], cipher[1], key[0])
    d = ECL.koblitz.decode(d, m[1])
    if d == message:
        print("test el_gamal_koblitz OK")
    else:
        print("test el_gamal_koblitzn ERROR")


def test_representation(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192):
    c = curve()
    p = point()
    c1 = eval(c.__repr__())
    p1 = eval(p.__repr__())
    if c1 == c and p1 == p:
        print("test representation OK")
    else:
        print("test representation ERROR")


def test_arithmetic(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192):
    inf = ECL.point.Point.infinitepoint(curve())
    p = point()
    cond1 = (p * 3) == ((p + p + p + p + p) - (p * 2))
    cond2 = (-p) == (inf - p)
    if not inf and cond1 and cond2:
        print("test arithmetic OK")
    else:
        print("test arithmetic ERROR")
