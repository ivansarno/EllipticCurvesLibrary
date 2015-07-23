from ECL import Auxfun

__author__ = 'ivansarno'
__version__ = 'V.2.3'
__doc__ = """ElGamal's cipher.

fun:
-keygen
-encrypt
-decrypt
"""


class EGmessage:
    """Cipher's message format.

    member: v, w
    :type v: Point
    :type w: Point
    """

    def __init__(self, vpoint, wpoint):
        """

        :param vpoint: Point to initialize v member
        :param wpoint: Point to initialize w member
        :type vpoint: Point
        :type wpoint: Point
        """
        self.v = vpoint
        self.w = wpoint


def keygen(bpoint, curve_size, generator=Auxfun.Generator()):
    """Cipher's key generator.

    :param bpoint: Point used as base, can be used a standard point from ECL_standardcurves
    :type bpoint: PointWOrder
    :rtype: EGkey
    :return: the key
    """
    secret = generator.get(curve_size) % bpoint.order
    kpoint = bpoint * secret
    return secret, kpoint


def encrypt(message, pubkey, stpoint, generator=Auxfun.Generator()):
    """ElGamal encryption fun.

    :param message: Point that expresses the message
    :param pubkey: Point used as public key
    :param stpoint: Point used as base, can be used a standard point from ECL_standardcurves
    :type message: Point
    :type pubkey: Point
    :type stpoint: Point
    :return: encrypted message
    :rtype: EGmessage
    """
    fact = generator.get(64)  # standard 64bit int
    vpoint = stpoint * fact
    wpoint = message + (pubkey * fact)
    return EGmessage(vpoint, wpoint)


def decrypt(message, privkey):
    """ElGamal decryption fun

    :type message: EGmessage
    :type privkey: Point
    :return: Point that expresses the message decrypted
    :rtype: Point
    """
    v = message.v * privkey
    v.negation()
    return message.w + v
