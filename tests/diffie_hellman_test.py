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
import ECL
from ECL import utility

__author__ = 'ivansarno'
__version__ = 'V.1.0'


def test_functionality() -> bool:
    user1 = ECL.DiffieHellman(ECL.std_curves.PointP192(), utility.generator)
    user2 = ECL.DiffieHellman(ECL.std_curves.PointP192(), utility.generator)
    message1 = user1.step1()
    message2 = user2.step1()
    user2.step2(message1)
    user1.step2(message2)
    return user1.key == user2.key


def test_synch_dh() -> bool:
    dh = ECL.DiffieHellman(ECL.std_curves.PointP192(), utility.generator)
    try:
        k = dh.key
        return False
    except ECL.diffie_hellman.DiffieHellmanError:
        pass

    try:
        dh.step2(ECL.std_curves.PointP192()._doubles())
        return False
    except ECL.diffie_hellman.DiffieHellmanError:
        pass
    return True


def test_dh() -> bool:
    return test_functionality() and test_synch_dh()
