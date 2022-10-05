from typing import List, Optional
import numpy as np

from ai.base.vector import Vector
from ai.models.anno import coco_anno_list as kps_anno


class Pose(object):
    def __init__(self, kps: List[List[float]]):
        self.data = np.array(kps)
        # Hip length is used to normalize the pose
        # self.norm_factor = np.linalg.norm(self.data[11] - self.data[12])

    def __getitem__(self, key: str):
        return self.data[kps_anno.index(key)]

    def kp_vector(self, key1: str, key2: str):
        return Vector(self[key1][..., :3], self[key2][..., :3])

    def similarity(self, other: 'Pose', template: str = 'skeletal_angle'):
        raise NotImplementedError

    def __repr__(self):
        return f'Pose({self.data})'


class PoseSeries(object):
    def __init__(self, poses: Optional[List[Pose]] = None):
        if poses is None:
            self.data = None
        if isinstance(poses, np.ndarray):
            self.data = poses
        elif isinstance(poses, list):
            if isinstance(poses[0], Pose):
                self.data = np.array([pose.data for pose in poses])
            else:
                self.data = np.vstack(np.array(poses))

    def __getitem__(self, slice):
        return self.data[slice]

    def kp_series(self, *key: List[str]):
        return PoseSeries(
            self.data[:, [kps_anno.index(k) for k in key], ...]
        )

    def joint_vector_series(self, key1: str, key2: str):
        return Vector(
            self.data[:, kps_anno.index(key1)][..., :3],
            self.data[:, kps_anno.index(key2)][..., :3]
        )

    @property
    def displacement(self):
        return self.data[-1] - self.data[0]

    def update(self, pose: Pose):
        if self.data is None:
            if pose.data.ndim < 3:
                self.data = np.array(pose.data)[None, ...]
            else:
                self.data = np.array(pose.data)
        else:
            self.data = np.concatenate(
                [self.data, pose.data[None, ...]], axis=0
            )
