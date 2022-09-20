from queue import Queue
from threading import Thread

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
        return self
    
    def run(self):
        '''
        Code to run the stream. This is where frames are fed to a queue.
        '''
        raise NotImplementedError

    @property
    def stopped(self):
        '''
        Check if the stream is stopped.
        '''
        return not self.thread.is_alive()

