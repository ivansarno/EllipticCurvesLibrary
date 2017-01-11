import ECL
from ECL import elgamal, utility, std_curves
import random

def point_test():
    point = ECL.std_curves.PointP192()
    dpoint = point._doubles()
    return point == eval(point.__repr__()) and dpoint == eval(dpoint.__repr__())

def elgamal_test():
    private = elgamal.PrivateKey.keygen(ECL.std_curves.PointP192(), utility.generator)
    public = private.public_key
    message = public.encrypt(random.randrange(1), utility.generator)
    rmessage = eval(message.__repr__())
    #r1 = message.first == rmessage.first and message.second == rmessage.second and message.padding == rmessage.padding
    rpublic = eval(public.__repr__())
    #r2 = public.
    rprivate = eval(private.__repr__())
    return vars(private) == vars(rprivate) and vars(message) == vars(rmessage) and vars(public) == vars(rpublic)


#def ecdsa_test():