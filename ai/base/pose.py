from typing import List, Optional
import numpy as np

from ai.base.vector import Vector
from ai.models.anno import coco_anno_list as kps_anno


class Pose(object):
    def __init__(self, kps: List[List[float]], frame_w: int = None, frame_h: int = None):
        """
        Takes a list of keypoints in the format: List[[x, y, z, vis]]
        and create a Pose object.
        self.data holds a numpy array of shape (17, 4).
        """
        self.data = np.array(kps)

        # Transformation to normal Euclidean space
        if frame_w is not None and frame_h is not None:
            scale = max(frame_w, frame_h)
            self.data[..., 0] *= frame_w/scale
            self.data[..., 1] *= frame_h/scale

    def __getitem__(self, key: str):
        return self.data[kps_anno.index(key)]

    def kp_vector(self, key1: str, key2: str):
        """
        Returns a vector between two keypoints by name.
        """
        return Vector(self[key1][..., :3], self[key2][..., :3])

    def similarity(self, other: 'Pose', template: str = 'skeletal_angle'):
        """
        A similarity metric between two poses.
        """
        raise NotImplementedError

    def __repr__(self):
        return f'Pose({self.data})'


class PoseSeries(object):
    def __init__(self, poses: Optional[List[Pose]] = None):
        """
        Takes a list of Pose, a list of 17x4 ndarrays, or a Nx17x4 ndarray
        and create a PoseSeries object.
        self.data holds a numpy array of shape (N, 17, 4).
        """
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
        """
        Returns a PoseSeries of the selected keypoints by name.
        Note that we can select multiple keypoints"""
        return PoseSeries(
            self.data[:, [kps_anno.index(k) for k in key], ...]
        )

    def joint_vector_series(self, key1: str, key2: str):
        """
        Returns a Vector object representing the series of vectors created
        by the selected 2 keypoints.
        """
        return Vector(
            self.data[:, kps_anno.index(key1)][..., :3],
            self.data[:, kps_anno.index(key2)][..., :3]
        )

    @property
    def displacement(self):
        """
        Returns [x, y, z] displacement of the pose series. Break if the first
        or last pose is a noise.
        """
        return self.data[-1] - self.data[0]

    def update(self, pose: Pose):
        """
        Update the internal series data with the new pose.
        """
        if self.data is None:
            if pose.data.ndim < 3:
                self.data = np.array(pose.data)[None, ...]
            else:
                self.data = np.array(pose.data)
        else:
            self.data = np.concatenate(
                [self.data, pose.data[None, ...]], axis=0
            )
