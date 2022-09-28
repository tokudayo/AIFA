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
    + Track position, velocity, acceleration of keypoints. Downside is if
    the HPE model is unstable, this will be too.
    - Evaluation for that part of exercise
    - Return a score for that part of exercise
    """
    def __init__(self, memory: int = 30, window_size: int = 10):
        self.kps = {}
        self.window_size = window_size
        self._count = window_size
        self.window = []
        self.prev_window = []
        for name in kps_anno.values():
            self.kps[name] = KeyPoint(name, memory)

    def update(self, kps: List[Tuple[float, float, float]]):
        """Pass normalized keypoints info in and update internal state"""
        if self._count == self.window_size:
            print(self.state)
            # Reset
            self.prev_window = self.window
            for name in kps_anno.values():
                self.kps[name] = KeyPoint(name, self.window_size - 1)
            self._count = 1

        for i, kp in enumerate(kps):
            self.kps[kps_anno[i]].update(*kp[:3])
        self._count += 1

    def evaluation(self):
        state = self.state()
        if state == 'start':
            return self._start()
        elif state == 'up':
            return self._up()
        elif state == 'down':
            return self._down()
        elif state == 'finish':
            return self._finish()

    @property
    def state(self):
        kps = self.kps
        print(kps['left_wrist'].displacement)
        if kps['left_wrist'].displacement[1] < -0.01:
            return 'up'
        elif kps['left_wrist'].displacement[1] > 0.01:
            return 'down'
        else:
            return 'none'
