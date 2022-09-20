import cv2
from .base import InputStream


class Cv2VideoStream(InputStream):
    '''
    Process video streams in a separate thread.
    '''
    def __init__(self, video_path, maxsize=30):
        super().__init__(maxsize=maxsize)
        self.video_path = video_path

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.queue.put(frame)
        cap.release()


class WebcamStream(InputStream):
    '''
    Process webcam stream. Need to manually call stop() to release the camera.
    '''
    def __init__(self, max_fps=30, maxsize=5):
        super().__init__(maxsize=maxsize)
        self.max_fps = max_fps
        self.cap = cv2.VideoCapture(0)
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._stop_signal = False

    def run(self):
        cap = self.cap
        while cap.isOpened() and not self._stop_signal:
            ret, frame = cap.read()
            if not ret:
                break
            try:
                self.queue.put(frame, block=False)
            except Exception:
                pass
        self.cap.release()

    def stop(self):
        self._stop_signal = True
        