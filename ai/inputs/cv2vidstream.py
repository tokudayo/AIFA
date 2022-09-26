import cv2

from ai.base import InputStream


class Cv2VideoStream(InputStream):
    '''
    Process video streams in a separate thread.
    '''
    def __init__(self, video_path: str, max_queue_size: int = 30):
        super().__init__(max_queue_size=max_queue_size)
        self.video_path = video_path

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.queue.put(frame)
        cap.release()
