__author__ = 'ivansarno'
from ECL_operator import *
import os

#define of constant and replaceable function

DH_Curve_size = 192 #size in bit integer in the operation

def randint():  #random number generator
    temp = os.urandom(DH_Curve_size // 8)
    return int.from_bytes(temp,'little')

class DH_Keycreator:
    def __init__(self, point):
        self.point=point

    def step1(self):
        self.secret = randint() % self.point.order
        return Product(self.point,self.secret)

    def step2(self,partnerpoint):
        self.key = Product(partnerpoint,self.secret)
        return self.key

    def returnkey(self):
        return self.key



















