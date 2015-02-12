__author__ = 'ivansarno'
from ECL_Auxfun import Inverse

class Curve:
    """Prime Elliptic Curve, parameters A and B, field Prime"""
    def __init__(self,a,b,p):
        self.A=a
        self.B=b
        self.Prime=p


class Point:
    """Point of Curve, parameters X,Y the curve of point and if is the infinite point"""
    def __init__(self,C,x,y):
        self.curve=C
        self.X=x
        self.Y=y
        self.infinite=False
    def Doubles(self):
        if not self.infinite:
            if self.Y==0:
                self.infinite=True
            else:
                lam=((3 * self.X**2 + self.curve.A) * Inverse(2 * self.Y, self.curve.Prime)) % self.curve.Prime
                x=((lam**2)-self.X-self.X) % self.curve.Prime
                y=(lam*(self.X-x)-self.Y) % self.curve.Prime
                self.Y=y
                self.X=x

    def Add(self,P):
        if not P.infinite:
            if self.infinite:
                self.infinite = False
                self.X = P.X
                self.Y = P.Y
            elif AreOpposites(self,P):
                self.infinite = True
            elif SamePoint(self,P):
                self.Doubles()
            else:
                lam=((P.Y-self.Y) * Inverse(P.X-self.X, self.curve.Prime)) % self.curve.Prime
                x=((lam**2)-self.X-P.X) % self.curve.Prime
                y=(lam*(self.X-x)-self.Y) % self.curve.Prime
                self.Y=y
                self.X=x

    def Opposite(self):
        self.Y = -self.Y % self.curve.Prime




def SameCurve(C1,C2):
    return (C1.A==C2.A) and (C1.B==C2.B) and (C1.Prime == C2.Prime)


def SamePoint(P1,P2):
    return (P1.X==P2.X) and (P1.Y==P2.Y) and SameCurve(P1.curve, P2.curve) and (P1.infinite==P2.infinite)



def AreOpposites(A,B):
    return (not A.infinite) and (not B.infinite) and SameCurve(A.curve,B.curve) and (A.X==B.Y) and (A.Y == -B.Y % B.curve.Prime)

class Point_wO (Point):
    """point with order"""
    def __init__(self,C,x,y,order):
        self.curve=C
        self.X=x
        self.Y=y
        self.infinite=False
        self.order = order


