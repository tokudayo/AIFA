from typing import List, Tuple

from ai.base import KeyPoint
from ai.models.anno import coco_anno as kps_anno


class Exercise():
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
            # Evaluate
            self.evaluation()
            # Reset
            self.prev_window = self.window
            for name in kps_anno.values():
                self.kps[name] = KeyPoint(name, self.window_size - 1)
            self._count = 1

        for i, kp in enumerate(kps):
            self.kps[kps_anno[i]].update(*kp[:3])
        self._count += 1

    def evaluation(self):
        raise NotImplementedError

    @property
    def state(self):
        raise NotImplementedError
