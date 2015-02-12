__author__ = 'ivansarno'
from ECL_class import *


def Duplication(A):
    """duplication of point of elliptic curve"""
    if A.infinite:
        return A
    elif A.Y == 0:
        A.infinite=True
        return A
    else:
        lam=((3 * A.X**2 + A.curve.A) * Inverse(2*A.Y, A.curve.Prime)) % A.curve.Prime
        x=((lam**2)-A.X-A.X) % A.curve.Prime
        y=(lam*(A.X-x)-A.Y) % A.curve.Prime
        P=Point(A.curve,x,y)
        return P


def Sum(A,B):
    """sum of point of elleiptic curve"""
    if A.infinite:
        return B
    elif B.infinite:
        return A
    elif SamePoint(A,B):
        return Duplication(A)
    elif AreOpposites(A,B):
        A.infinite = True
        return A
    else:
        lam=((B.Y-A.Y) * Inverse(B.X-A.X, A.curve.Prime)) % A.curve.Prime
        x=((lam**2)-A.X-B.X) % A.curve.Prime
        y=(lam*(A.X-x)-A.Y) % A.curve.Prime
        P=Point(A.curve,x,y)
        return P


def Negation(P):
    """aritmetic negation of a point"""
    ris = Point(P.curve,P.X,-P.Y % P.curve.Prime)
    return ris

def Copy(P):
    ris = Point(P.curve,P.X,P.Y)
    return ris


def Product(point, num):
    if num >= 2 and (not point.infinite):
      temp = Copy(point)
      pointlist = [point]
      i = 1
      j = 0
      while (i < num):
          j = j+1
          i = 2 * i
          temp.Doubles()
          pointlist.append(Copy(temp))
      temp.infinite = True
      while(num > 0):
          if num - i >=0:
              temp.Add(pointlist[j])
              num = num - i
          j = j - 1
          i = i // 2
      return temp
    else:
        return Copy(point)
