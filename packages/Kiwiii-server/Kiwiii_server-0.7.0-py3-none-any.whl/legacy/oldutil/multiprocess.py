
# TODO: no longer used

import os
import pickle
import multiprocessing as mp


def queue(func):
    """ Decorator
    execute function on a temporary process
    result is passed by using Queue
    """
    def _f(*args, **kwargs):
        def _p(*args, **kwargs):
            al = list(args)
            q = al.pop()
            q.put(func(*al, **kwargs))
        queue = mp.Queue()
        argsl = list(args)
        argsl.append(queue)
        proc = mp.Process(target=_p, args=argsl, kwargs=kwargs)
        proc.start()
        proc.join()
        return queue.get()
    return _f


def ipc_run(func):
    """ Execute function on a temporary child process.
    result will be passed to parent by using temporary file.
    As _f function is not picklable, this method is not suitable for Windows
    which uses 'spawn' command to generate child process.
    """
    def _f(*args, **kwargs):
        def _p(*args, **kwargs):
            al = list(args)
            n = al.pop()
            res = func(*al, **kwargs)
            with open(n, "wb") as f:
                pickle.dump(res, f)
        tmp_name = "_tmp.pickle"
        argsl = list(args)
        argsl.append(tmp_name)
        proc = mp.Process(target=_p, args=argsl, kwargs=kwargs)
        proc.start()
        proc.join()
        with open(tmp_name, "rb") as f:
            result = pickle.load(f)
        os.remove(tmp_name)
        return result
    return _f


class FileBasedIPC(object):
    """ Windows compatible file-based IPC
    """
    def __init__(self, func):
        self.func = func

    def _f(self, *args, **kwargs):
        tmp_name = "_tmp.pickle"
        argsl = list(args)
        argsl.append(tmp_name)
        proc = mp.Process(target=self._p, args=argsl, kwargs=kwargs)
        proc.start()
        proc.join()
        with open(tmp_name, "rb") as f:
            result = pickle.load(f)
        os.remove(tmp_name)
        return result

    def _p(self, *args, **kwargs):
        al = list(args)
        n = al.pop()
        res = self.func(*al, **kwargs)
        with open(n, "wb") as f:
            pickle.dump(res, f)

    def __call__(self):
        return self._f
