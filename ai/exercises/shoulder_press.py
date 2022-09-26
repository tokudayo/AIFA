from typing import List, Tuple

from ai.base import KeyPoint


kps_anno = {
    0: 'nose',
    1: 'left_eye',
    2: 'right_eye',
    3: 'left_ear',
    4: 'right_ear',
    5: 'left_shoulder',
    6: 'right_shoulder',
    7: 'left_elbow',
    8: 'right_elbow',
    9: 'left_wrist',
    10: 'right_wrist',
    11: 'left_hip',
    12: 'right_hip',
    13: 'left_knee',
    14: 'right_knee',
    15: 'left_ankle',
    16: 'right_ankle',
}


class ShoulderPress():
    """
    Needs to:
    - Somehow detect what part of exercise is being performed by:
    + Tracking position, velocity, acceleration of keypoints. Downside is if
    the HPE model is unstable, this will be too.
    - Evaluation for that part of exercise
    - Return a score for that part of exercise"""
    def __init__(self, memory: int = 30):
        self.kps = {}
        for name in kps_anno.values():
            self.kps[name] = KeyPoint(name, memory)

    def update(self, kps: List[Tuple[float, float, float]]):
        """Pass normalized keypoints info in and update internal state"""
        for i, kp in enumerate(kps):
            self.kps[kps_anno[i]].update(*kp[:3])

    @property
    def state(self):
        print(self.kps['left_elbow'].position)
        kps = self.kps
        if kps['left_elbow'].velocity[1] < -0.005:
            return 'up'
        elif kps['left_elbow'].velocity[1] > 0.005:
            return 'down'
        else:
            return 'none'
