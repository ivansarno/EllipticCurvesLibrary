__author__ = 'ivansarno'
from ECL_operator import *
import os

#define of constant and replaceable function

DH_Curve_size = 192 #size in bit integer in the operation

def randint():  #random number generator for point of curve factor
    temp = os.urandom(DH_Curve_size // 8)
    return int.from_bytes(temp,'little')

def randfact():  #random number generator for message point factor
    temp = os.urandom(8)
    return int.from_bytes(temp,'little')

class EG_Key:
    def __init__(self,priv,pub):
        self.public = pub
        self.private = priv

class EG_Message:
    def __init__(self,vpoint,wpoint):
        self.v = vpoint
        self.w = wpoint



def eg_keygen(bpoint):
    secret = randint() % bpoint.order
    kpoint = Product(bpoint,secret)
    return EG_Key(secret, kpoint)



def eg_encrypt(message,key,stpoint):
    fact= randfact()
    Vpoint = Product(stpoint,fact)
    Wpoint = Sum(message,Product(key,fact))
    return EG_Message(Vpoint,Wpoint)


def eg_decrypt(message,key):
    V = Product(message.v,key.private)
    V.Opposite()
    return Sum(message.w,V)





