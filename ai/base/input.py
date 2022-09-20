from queue import Queue
from threading import Thread
import time


class InputStream(object):
    def __init__(self, maxsize=30):
        '''
        All frames should be dumped into a queue for further processing.
        '''
        self.queue = Queue(maxsize=maxsize)
    
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
        '''
        raise NotImplementedError

    def get_frame(self, block=True, timeout=1.):
        '''
        Get a frame from the queue. Default to blocking with 1s timeout.
        '''
        try:
            frame = self.queue.get(block=block, timeout=timeout)
        except:
            return None
        return frame

    @property
    def stopped(self):
        '''
        Check if the stream is stopped.
        '''
        return not self.thread.is_alive()

