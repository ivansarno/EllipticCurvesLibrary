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
from ECL import ecdsa
from ECL import std_curves
from ECL import utility
from ECL.ecdsa import *

__author__ = 'ivansarno'
__version__ = 'V.1.0'


def test_functionality() -> bool:
    base = std_curves.PointP192()
    private = PrivateKey.keygen(base, utility.generator)
    public = private.public_key
    message = bytearray(random.randrange(1, 1000000))
    signature = private.sign(message, utility.generator)
    # true signature check
    if not public.check(message, signature):
        return False
    # fake signatures check, should not be recognized
    fake_signature = Signature(signature.first + 1, signature.second)
    if public.check(message, fake_signature):
        return False
    fake_signature = Signature(signature.first, signature.second - 1)
    if public.check(message, fake_signature):
        return False
    fake_signature = Signature(signature.first, 0)
    if public.check(message, fake_signature):
        return False
    fake_signature = Signature(signature.first, base.order + 1)
    if public.check(message, fake_signature):
        return False
    fake_signature = Signature(0, signature.second)
    if public.check(message, fake_signature):
        return False
    fake_signature = Signature(base.order + 1, signature.second)
    if public.check(message, fake_signature):
        return False
    return True


def test_rapresentation() -> bool:
    private = PrivateKey.keygen(std_curves.PointP192(), utility.generator)
    public = private.public_key
    message = bytearray(random.randrange(1, 10000000))
    signature = private.sign(message, utility.generator)
    if not vars(signature) == vars(eval(signature.__repr__())):
        return False
    if not vars(public) == vars(eval(public.__repr__())):
        return False
    if not vars(private) == vars(eval(private.__repr__())):
        return False
    return True


def test_key_creation() -> bool:
    try:
        key1 = ecdsa.PrivateKey.keycreate(ECL.std_curves.PointP192(), -342)
        key2 = ecdsa.PrivateKey.keycreate(ECL.std_curves.PointP192(), 1)
        return False
    except ECDSAError:
        pass
    secret = utility.generator(192)
    private = ecdsa.PrivateKey.keycreate(ECL.std_curves.PointP192(), secret)
    public = private.public_key
    rprivate = public.try_unlock_key(-3523)
    if not rprivate is None:
        return False
    rprivate = public.try_unlock_key(1)
    if not rprivate is None:
        return False
    rprivate = public.try_unlock_key(secret + 1)
    if not rprivate is None:
        return False
    rprivate = public.try_unlock_key(secret)
    if rprivate == private:
        return False
    return True


def test_ecdsa() -> bool:
    return test_functionality() and test_functionality() and test_key_creation()
