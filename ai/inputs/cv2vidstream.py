import cv2

from ai.base import InputStream


class Cv2VideoStream(InputStream):
    '''
    Process video streams in a separate thread.
    '''
    def __init__(self,
                 video_path: str,
                 max_queue_size: int = 30,
                 max_size: int = 540):
        super().__init__(max_queue_size=max_queue_size)
        self.video_path = video_path
        self.max_size = max_size

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
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
        cap.release()
