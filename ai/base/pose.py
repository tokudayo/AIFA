from typing import List
import numpy as np

from ai.base.vector import Vector
from models.anno import coco_anno_list as kps_anno


class Pose(object):
    def __init__(self, kps: List[List[float]]):
        self.kps = np.array(kps)
        # Hip length is used to normalize the pose
        self.norm_factor = np.linalg.norm(self.kps[11] - self.kps[12])

    def __getitem__(self, key: str):
        return self.kps[kps_anno.index(key)].squeeze()

    def to_vector(self, key1: str, key2: str):
        return Vector(self[key1], self[key2])
