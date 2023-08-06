
class Singleton(object):

    def __init__(self):
        raise IOError("hugahuga")

    def hoge(self):
        print "singleton!"

INSTANCE = Singleton()


if __name__ == "__main__":
    from tmp.singletontest import INSTANCE as OBJ1
    from tmp.singletontest import INSTANCE as OBJ2
    OBJ1.hoge()
    OBJ2.hoge()
    if OBJ1 is OBJ2:
        print "onaji"
    else:
        print "chigau"
