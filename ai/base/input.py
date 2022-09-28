from queue import Queue
from threading import Thread


class InputStream(object):
    def __init__(self, max_queue_size: int = 30):
        '''
        All frames should be dumped into a queue for further processing.
        '''
        self.queue = Queue(maxsize=max_queue_size)
        self._stop_signal = False

    def start(self):
        '''
        Start a input stream thread.
        '''
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        '''
        Code to run the stream. This is where frames are fed to a queue.
        Must response to stop signal.
        '''
        raise NotImplementedError

    def get_frame(self, block: bool = True, timeout: float = 1.):
        '''
        Get a frame from the queue. Default to blocking with 1s timeout.
        '''
        try:
            frame = self.queue.get(block=block, timeout=timeout)
        except Exception:
            return None
        return frame

    def stop(self):
        self._stop_signal = True

    @property
    def stopped(self):
        '''
        Check if the stream is stopped.
        '''
        return not self.thread.is_alive()
