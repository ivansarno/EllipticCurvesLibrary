import random

from ECL import std_curves
from ECL import utility
from ECL.ecdsa import *

def test_functionality() -> bool:
    base = std_curves.PointP192()
    private = PrivateKey.keygen(base, utility.generator)
    public = private.public_key
    message = message = bytearray(random.randrange(1))
    signature = private.sign(message, utility.generator)
    #true signature check
    if not public.check(message, signature):
        return False
    #fake signatures check, should not be recognized
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
    message = bytearray(random.randrange(1))
    signature = private.sign(message, utility.generator)
    if not vars(signature) == vars(eval(signature.__repr__())):
        return False
    if not vars(public) == vars(eval(public.__repr__())):
        return False
    if not vars(private) == vars(eval(private.__repr__())):
        return False
    return True


def test() -> bool:
    return test_functionality() and test_functionality()



