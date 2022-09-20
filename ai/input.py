import cv2
from .base import InputStream


class Cv2VideoStream(InputStream):
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