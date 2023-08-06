
from PySide import QtCore, QtGui


class Thread(QtCore.QThread):

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.worker = None

    def launch_worker(self, worker):
        self.main.status_bar.start_process()
        self.main.threads.append(self)
        self.worker = worker
        self.worker.moveToThread(self)
        self.worker.finished.connect(self.quit)
        self.start()

    def quit(self):
        self.main.threads.remove(self)
        super().quit()

    def abort(self):
        self.worker.invoke_method("abort")
        self.quit()
        self.wait()


class WorkerObject(QtCore.QObject):

    finished = QtCore.Signal()

    def __init__(self):
        super().__init__()

    def invoke_method(self, method):
        if self.thread() is QtGui.QApplication.instance().thread():
            QtCore.QMetaObject.invokeMethod(
                self, method, QtCore.Qt.DirectConnection)
        else:
            QtCore.QMetaObject.invokeMethod(
                self, method, QtCore.Qt.QueuedConnection)

    def abort(self):
        raise NotImplementedError()
