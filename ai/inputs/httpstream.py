from typing import Optional
import cv2
import numpy as np
import requests

from ai.base import InputStream


class HTTPStream(InputStream):
    '''
    Process from HTTP stream, per-frame processing.
    '''
    def __init__(
            self, 
            url: str = 'http://192.168.1.1:8080/shot.jpg',
            width: Optional[int] = 640, 
            height: Optional[int] = 480,
            max_queue_size=5):
        '''
        Assuming the HTTP stream is from an IP camera, which gives a JPEG image for each request.
        '''
        super().__init__(max_queue_size=max_queue_size)
        self.width, self.height = width, height
        self.url = url

    def run(self):
        while not self._stop_signal:
            # Get image from HTTP stream
            try:
                img_resp = requests.get(self.url)
            except Exception:
                continue
            if img_resp.status_code != 200:
                continue
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
            if self.width is not None and self.height is not None:
                frame = cv2.resize(frame, (self.width, self.height))
            try:
                self.queue.put(frame, block=False)
            except Exception:
                pass
