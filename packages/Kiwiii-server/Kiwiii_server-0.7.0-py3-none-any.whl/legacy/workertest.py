from concurrent.futures import ProcessPoolExecutor
import time

from tornado import ioloop, gen
from tornado.queues import Queue


class WorkerQueue(object):
    def __init__(self):
        self.queue = Queue()
        self.current_worker_id = None
        self.current_worker = None
        self.queued_ids = []
        self._dispatcher()

    def put(self, id_, func, args):
        worker = Worker(func, args)
        self.queued_ids.append(id_)
        self.queue.put_nowait((id_, worker))
        print("Put: {}".format(id_))

    def status(self, id_):
        if id_ in self.queued_ids:
            return "Queued"
        elif id_ == self.current_worker_id:
            return "Running"
        else:
            return "Ready"

    @gen.coroutine
    def _dispatcher(self):
        while 1:
            id_, worker = yield self.queue.get()
            self.queued_ids.remove(id_)
            self.current_worker_id = id_
            self.current_worker = worker
            print("Start: {}".format(id_))
            res = yield self.current_worker.execute()
            self.current_worker_id = None
            self.current_worker = None
            print("{} is {}.".format(id_, res))


class Worker(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    @gen.coroutine
    def execute(self):
        with ProcessPoolExecutor(1) as exec_:
            res = yield exec_.submit(self.func, *self.args)
        return res


def job(sec):
    time.sleep(sec)
    return "done"


@gen.coroutine
def run():
    q = WorkerQueue()
    q.put("Job1", job, (2,))
    q.put("Job2", job, (2,))
    print("Job1 <{}>".format(q.status("Job1")))
    print("Job2 <{}>".format(q.status("Job2")))
    yield gen.sleep(1)
    print("Job1 <{}>".format(q.status("Job1")))
    print("Job2 <{}>".format(q.status("Job2")))
    yield gen.sleep(2)
    print("Job1 <{}>".format(q.status("Job1")))
    print("Job2 <{}>".format(q.status("Job2")))
    yield gen.sleep(2)
    print("Job1 <{}>".format(q.status("Job1")))
    print("Job2 <{}>".format(q.status("Job2")))


if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(run)
