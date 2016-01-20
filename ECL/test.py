"""
    Elliptic Curve Library

    Copyright 2015 Ivan Sarno

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import random
import ECL
from ECL import *
from ECL import utility, ecdsa

__author__ = 'ivansarno'
__version__ = 'V.5.0'
__doc__ = """Test for package's features"""


def test(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192, generator=utility.generator) -> bool:
    try:
        result = test_arithmetic(curve, point)
        result &= test_diffie_hellman(point, generator)
        result &= test_el_gamal_koblitz(curve, point, generator)
        result &= test_representation(curve, point)
        result &= test_ecdsa(generator=generator)
    except ECL.EclException:
        print("test ERROR: EclException Raised")
        return False
    except Exception:
        print("test ERROR: Other Exception Raised")
        return False
    return result


def test_diffie_hellman(point=ECL.std_curves.PointP192, generator=utility.generator):
    user1 = ECL.DiffieHellman(point(), generator)
    user2 = ECL.DiffieHellman(point(), generator)
    message1 = user1.step1()
    message2 = user2.step1()
    user2.step2(message1)
    user1.step2(message2)
    if user1.key == user2.key:
        print("test diffie-hellman OK")
        return True
    else:
        print("test diffie-hellman ERROR")
        return False


def test_el_gamal_koblitz(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192, generator=utility.generator):
    key = ECL.elgamal.keygen(point(), generator)
    message = random.randint(0, 65535)
    m = ECL.koblitz.iterative_encode(message, curve())
    cipher = ECL.elgamal.encrypt(m[0], key[1], point(), generator)
    d = ECL.elgamal.decrypt(cipher[0], cipher[1], key[0])
    d = ECL.koblitz.decode(d, m[1])
    if d == message:
        print("test el_gamal_koblitz OK")
        return True
    else:
        print("test el_gamal_koblitzn ERROR")
        return False


def test_representation(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192):
    c = curve()
    p = point()
    c1 = eval(c.__repr__())
    p1 = eval(p.__repr__())
    if c1 == c and p1 == p:
        print("test representation OK")
        return True
    else:
        print("test representation ERROR")
        return False


def test_arithmetic(curve=ECL.std_curves.CurveP192, point=ECL.std_curves.PointP192):
    inf = ECL.point.Point.infinitepoint(curve())
    p = point()
    cond1 = (p * 3) == ((p + p + p + p + p) - (p * 2))
    cond2 = (-p) == (inf - p)
    if not inf and cond1 and cond2:
        print("test arithmetic OK")
        return True
    else:
        print("test arithmetic ERROR")
        return False


def test_ecdsa(message: bytearray=None, point=ECL.std_curves.PointP192, generator=utility.generator):
    p = point()
    if message is None:
        message = generator(2000)
        message = message.to_bytes(message.bit_length()//8 + 1, 'little')
    k = ecdsa.keygen(p, utility.generator)
    f = ecdsa.sign(message, k[0], p, generator)
    if not ecdsa.check(message, f[0], f[1], k[1], p):
        print("test ecdsa ERROR")
        return False
    f = (utility.generator(80), generator(80))
    if ecdsa.check(message, f[0], f[1], k[1], p):
        print("test ecdsa ERROR")
        return False
    print("test ecdsa OK")
    return True
