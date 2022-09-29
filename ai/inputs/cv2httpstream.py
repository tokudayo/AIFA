from typing import Optional
import cv2
import numpy as np
import requests
import time

from ai.base import InputStream


class Cv2HTTPStream(InputStream):
    '''
    Process from HTTP stream, which should be a video stream.
    '''
    def __init__(
            self,
            url: str = 'http://192.168.1.113:8080/video',
            width: Optional[int] = 640,
            height: Optional[int] = 480,
            max_size: int = 540,
            max_queue_size=5):
        super().__init__(max_queue_size=max_queue_size)
        self.width, self.height = width, height
        self.max_size = max_size
        self.cap = cv2.VideoCapture(url)

    def run(self):
        cap = self.cap
        while cap.isOpened() and not self._stop_signal:
            ret, frame = cap.read()
            if not ret:
                break
            if max(frame.shape) > self.max_size:
                scale_factor = self.max_size / max(frame.shape)
                frame = cv2.resize(
                    frame, None, fx=scale_factor, fy=scale_factor
                )
                frame = cv2.flip(frame, 0)
            try:
                self.queue.put(frame, block=False)
            except Exception:
                pass
        self.cap.release()
