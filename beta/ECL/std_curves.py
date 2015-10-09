from ECL.curve import Curve
from ECL.point_with_order import PointWOrder

__author__ = 'ivansarno'
__version__ = 'V.4.beta'
__doc__ = """Nist's standard curves and points

(the number in the name is the bit of order)
Points: PointP192, PointP224, PointP256, PointP384, PointP521
Curves: CurveP192, CurveP225, CurveP256, CurveP384, CurveP521

"""


class CurveP192(Curve):
    def __init__(self):
        a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
        b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
        prime = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
        super().__init__(a, b, prime)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class PointP192(PointWOrder):
    def __init__(self):
        x = 0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012
        y = 0x7192b95ffc8da78631011ed6b24cdd573f977a11e794811
        order = 0xffffffffffffffffffffffff99def836146bc9b1b4d22831
        curve = CurveP192()
        super().__init__(curve, x, y, order)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class CurveP224(Curve):
    def __init__(self):
        a = 0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe
        b = 0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4
        prime = 0xffffffffffffffffffffffffffffffff000000000000000000000001
        super().__init__(a, b, prime)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class PointP224(PointWOrder):
    def __init__(self):
        x = 0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21
        y = 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34
        order = 0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d
        curve = CurveP224()
        super().__init__(curve, x, y, order)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class CurveP256(Curve):
    def __init__(self):
        a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
        b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        prime = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        super().__init__(a, b, prime)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class PointP256(PointWOrder):
    def __init__(self):
        x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
        y = 0xfe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
        order = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
        curve = CurveP256()
        super().__init__(curve, x, y, order)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class CurveP384(Curve):
    def __init__(self):
        a = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000fffffffc
        b = 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef
        prime = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff
        super().__init__(a, b, prime)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class PointP384(PointWOrder):
    def __init__(self):
        x = 0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7
        y = 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f
        order = 0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973
        curve = CurveP384()
        super().__init__(curve, x, y, order)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class CurveP521(Curve):
    def __init__(self):
        a = 0x1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc
        b = 0x51953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
        prime = 0x1ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        super().__init__(a, b, prime)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()


class PointP521(PointWOrder):
    def __init__(self):
        x = 0xc6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66
        y = 0x11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650
        order = 0x1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409
        curve = CurveP521()
        super().__init__(curve, x, y, order)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
