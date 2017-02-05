import ECL
from ECL import utility


def test_functionality() -> bool:
    user1 = ECL.DiffieHellman(ECL.std_curves.PointP192(), utility.generator)
    user2 = ECL.DiffieHellman(ECL.std_curves.PointP192(), utility.generator)
    message1 = user1.step1()
    message2 = user2.step1()
    user2.step2(message1)
    user1.step2(message2)
    return user1.key == user2.key


def test_synch_dh() -> bool:
    dh = ECL.DiffieHellman(ECL.std_curves.PointP192(), utility.generator)
    r = False
    try:
        k = dh.key
    except ECL.diffie_hellman.DiffieHellmanError:
        r = True

    try:
        dh.step2(ECL.std_curves.PointP192()._doubles())
        r &= False
    except ECL.diffie_hellman.DiffieHellmanError:
        r &= True
    return r


def test() -> bool:
    return test_functionality() and test_synch_dh()
