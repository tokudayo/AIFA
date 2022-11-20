import time


class Timer(object):
    def __init__(self):
        self._start = None
        self._end = None

    def start(self):
        self._start = time.perf_counter()

    def stop(self):
        self._end = time.perf_counter()

    @property
    def elapsed(self):
        return self._end - self._start
