from typing import List
import numpy as np

from ai.base.vector import Vector
from ai.models.anno import coco_anno_list as kps_anno


skeletal_angle_template = [
    [5, 6],
    [6, 8],
    [5, 7],
    [8, 10],
    [7, 9],
]


class Pose(object):
    def __init__(self, kps: List[List[float]]):
        self.data = np.array(kps)
        # Hip length is used to normalize the pose
        self.norm_factor = np.linalg.norm(self.data[11] - self.data[12])

    def __getitem__(self, key: str):
        return self.data[kps_anno.index(key)]

    def kp_vector(self, key1: str, key2: str):
        return Vector(self[key1][..., :3], self[key2][..., :3])

    def similarity(self, other: 'Pose', template: str = 'skeletal_angle'):
        if template == 'skeletal_angle':
            return self.skeletal_angle_similarity(other)
        else:
            raise NotImplementedError

    def skeletal_angle_similarity(self, other: 'Pose'):
        """
        Calculate the similarity between two poses based on skeletal angle.
        """
        # Normalize the pose
        self_norm = self.data / self.norm_factor
        other_norm = other.data / other.norm_factor

        # Calculate the skeletal angle
        self_angle = self.skeletal_angle()
        other_angle = other.skeletal_angle()

        # Calculate the similarity
        return np.mean(np.abs(self_angle - other_angle))

    def __repr__(self):
        return f'Pose({self.data})'


class PoseSeries(object):
    def __init__(self, poses: List[Pose]):
        if isinstance(poses, np.ndarray):
            self.data = poses
        elif isinstance(poses, list):
            if isinstance(poses[0], Pose):
                self.data = np.array([pose.data for pose in poses])
            elif isinstance(poses[0], np.ndarray):
                self.data = poses

    def __getitem__(self, slice):
        return self.data[slice]

    def kp_series(self, key: str):
        return self.data[:, kps_anno.index(key)]

    def kp_vector_series(self, key1: str, key2: str):
        return Vector(self.kp_series(key2)[..., :3], self.kp_series(key1)[..., :3])

    def update(self, pose: Pose):
        self.data = np.append(self.data, pose.data)
