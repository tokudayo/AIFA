import cv2

from ai.base import InputStream


class Cv2WebcamStream(InputStream):
    '''
    Process webcam stream. Need to manually call stop() to release the camera.
    '''
    def __init__(self, max_fps: int = 30, max_queue_size: int = 5):
        super().__init__(max_queue_size=max_queue_size)
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