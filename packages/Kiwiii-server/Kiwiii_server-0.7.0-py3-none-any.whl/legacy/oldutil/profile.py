
# TODO: no longer used

import cProfile
import pstats


def profile(func):
    """ Decorator
    execute cProfile
    """
    def _f(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        print("\n<<<---")
        res = func(*args, **kwargs)
        p = pstats.Stats(pr)
        p.strip_dirs().sort_stats('cumtime').print_stats(20)
        print("\n--->>>")
        return res
    return _f
