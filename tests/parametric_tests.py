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
from ECL import Point
from ECL import PointWOrder
from ECL import utility, ecdsa, elgamal

__author__ = 'ivansarno'
__version__ = 'V.1.0'
__doc__ = """Test for package's features"""


def test(point: PointWOrder=ECL.std_curves.PointP192(), generator=utility.generator) -> bool:
    try:
        result = test_arithmetic(point.copy())
        result &= test_diffie_hellman(point.copy(), generator)
        result &= test_el_gamal_koblitz(point.copy(), generator)
        result &= test_ecdsa(generator=generator)
    except ECL.EclError:
        print("test ERROR: EclException Raised")
        return False
    except Exception:
        print("test ERROR: Other Exception Raised")
        return False
    return result


def test_diffie_hellman(point: PointWOrder=ECL.std_curves.PointP192(), generator=utility.generator) -> bool:
    user1 = ECL.DiffieHellman(point, generator)
    user2 = ECL.DiffieHellman(point, generator)
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


def test_el_gamal_koblitz(point: PointWOrder=ECL.std_curves.PointP192(), generator=utility.generator) -> bool:
    private = elgamal.PrivateKey.keygen(point, generator)
    public = private.public_key
    message = random.randint(1, 2**32)
    cipher = public.encrypt(message, generator)
    cipher = private.decrypt(cipher)
    if cipher == message:
        print("test el_gamal_koblitz OK")
        return True
    else:
        print("test el_gamal_koblitz ERROR")
        return False


def test_arithmetic(point: Point) -> bool:
    inf = point.infinitepoint(point.curve)
    if point != (point + inf) or point != (point - inf):
        print("test arithmetic ERROR")
        return False
    p = point.copy()
    p._doubles()
    inf2 = inf.copy()
    inf2._doubles()
    if point + point != p or inf2 != inf:
        print("test arithmetic ERROR")
        return False
    if -point != inf - point:
        print("test arithmetic ERROR")
        return False
    a = random.randrange(500)
    b = random.randrange(a // 2)
    p = inf.copy()
    for i in range(0, a):
        p += point
    if point * a != p:
        print("test arithmetic ERROR")
        return False
    if point * (a - b) != (point * a) - (point * b):
        return False
    print("test arithmetic OK")
    return True


def test_ecdsa(message: bytearray=None, point: PointWOrder=ECL.std_curves.PointP192(), generator=utility.generator) -> bool:
    if message is None:
        message = generator(2000)
        message = message.to_bytes(message.bit_length()//8 + 1, 'little')
    priv = ecdsa.PrivateKey.keygen(point, generator)
    pub = priv.public_key
    sign = priv.sign(message, generator)
    if not pub.check(message, sign):
        print("test ecdsa ERROR")
        return False
    fake = ecdsa.Signature(sign.first-1, sign.second-1)
    if pub.check(message, fake):
        print("test ecdsa ERROR")
        return False
    print("test ecdsa OK")
    return True
