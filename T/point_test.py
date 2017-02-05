import ECL
from ECL import elgamal, utility, std_curves
import random

def point_test():
    point = ECL.std_curves.PointP192()
    dpoint = point._doubles()
    return point == eval(point.__repr__()) and dpoint == eval(dpoint.__repr__())




