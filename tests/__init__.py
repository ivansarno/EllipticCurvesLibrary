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
from tests import diffie_hellman_test, ecdsa_test, elgamal_test, koblitz_test, point_test, utility_test
__author__ = 'ivansarno'
__version__ = 'V.1.0'


def ecl_test():
    return diffie_hellman_test.test_dh() and ecdsa_test.test_ecdsa() and elgamal_test.test_elgamal() and koblitz_test.test_koblitz() \
           and point_test.test_point() and utility_test.test_utility()
