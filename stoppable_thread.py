import threading

class StoppableThread(threading.Thread):

    def __init__(self, st_name=None, st_target=None, st_args=None):
        super(StoppableThread, self).__init__(name=st_name,
            target=st_target, args=st_args)
        self._stop() = threading.Event()

    def stop(self):
        self._stop().set()

    def is_stopped(self):
        return self._stop.is_set()