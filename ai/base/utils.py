import time
import numpy as np

class Timer(object):
    def __init__(self):
        self._start = None
        self._end = None

    def start(self):
        self._start = time.perf_counter()

    def stop(self):
        self._end = time.perf_counter()

    @property
    def elapsed(self):
        return self._end - self._start
    

def blazepose_kp_to_coco_kp(landmarks):
    '''
    This function converts the 33 keypoints to 17 keypoints:
            
            "nose","left_eye","right_eye","left_ear","right_ear",
            "left_shoulder","right_shoulder","left_elbow","right_elbow",
            "left_wrist","right_wrist","left_hip","right_hip",
            "left_knee","right_knee","left_ankle","right_ankle"

    Each formatted as follow, according to COCO format:
            [x, y, visibility]
        '''
    # idx of needed keypoints in BlazePose
    idx = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
    # Filter out the keypoints
    landmarks = [landmarks[i] for i in idx]
    # Convert to COCO format
    landmarks = [[landmark.x, landmark.y, landmark.visibility] for landmark in landmarks]

    return landmarks