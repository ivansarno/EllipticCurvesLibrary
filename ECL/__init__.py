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
from ECL import point, curve, std_curves, point_with_order, koblitz, elgamal, diffie_hellman, ecdsa
from ECL.curve import Curve
from ECL.point import Point
from ECL.utility import EclException
from ECL.diffie_hellman import DiffieHellman
from ECL.point_with_order import PointWOrder

__author__ = 'ivansarno'
__version__ = 'V.5.1'
__all__ = ["Curve", "Point", "PointWOrder", "EclException"]
__doc__ = """ ECL: library includes basic operations on Elliptic curves, 2 cipher and a digital signature protocol.

includes:
class: Point, PointWOrder, Curve
algorithm: Diffie-Hellman, ElGamal, Koblitz, ECDSA
built-in: Nist's standard curves and points
exception: EclException, DiffieHellmanError, KoblitzFailError, ECDSAError, ElGamalError
"""