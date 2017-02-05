"""
    Elliptic Curve Library

    Copyright 2017 Ivan Sarno

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
from ECL import elgamal, utility
from ECL.elgamal import ElGamalError

__author__ = 'ivansarno'
__version__ = 'V.5.4'


def test_functionality() -> bool:
    private = elgamal.PrivateKey.keygen(ECL.std_curves.PointP192(), utility.generator)
    public = private.public_key
    message = random.randrange(1)
    cipher = public.encrypt(message, utility.generator)
    cipher = private.decrypt(cipher)
    return cipher == message


def test_out_of_range() -> bool:
    public = elgamal.PrivateKey.keygen(ECL.std_curves.PointP192(), utility.generator).public_key
    message = ECL.std_curves.PointP192().order + 200
    try:
        cipher = public.encrypt(message, utility.generator)
        return False
    except ElGamalError:
        return True


def test_rapresentation() -> bool:
    private = elgamal.PrivateKey.keygen(ECL.std_curves.PointP192(), utility.generator)
    public = private.public_key
    message = public.encrypt(random.randrange(1), utility.generator)
    rmessage = eval(message.__repr__())
    rpublic = eval(public.__repr__())
    rprivate = eval(private.__repr__())
    return vars(private) == vars(rprivate) and vars(message) == vars(rmessage) and vars(public) == vars(rpublic)


def test() -> bool:
    return test_functionality() and test_out_of_range() and test_rapresentation()
