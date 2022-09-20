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
    Process webcam stream.
    '''
    def __init__(self, max_fps=30, maxsize=30):
        super().__init__(maxsize=maxsize)
        self.max_fps = max_fps
        self.cap = cv2.VideoCapture(0)
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            self.queue.put(frame)
    
    def release_cam(self):
        self.cap.release()
