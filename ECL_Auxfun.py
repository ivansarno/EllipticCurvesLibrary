__author__ = 'ivansarno'
#implementation of Extended Euclide algorithm and inverse in modulo calculation

def ExtendedEuclide(a,b):
    if b==0:
        return (a,1,0)
    temp=ExtendedEuclide(b, a%b)
    return (temp[0],temp[2],temp[1]-((a//b)*temp[2]))

def Inverse(a,b):
    temp=ExtendedEuclide(a,b)
    return temp[1]
