import math
from typing import List, Optional
import numpy as np

from aifa.base.vector import Vector
from aifa.utils import rad_to_deg
from aifa.utils.anno import coco_anno_list as kps_anno

lines = {
    'lr_shoulder': ['left_shoulder', 'right_shoulder'],
    'l_side': ['left_shoulder', 'left_hip'],
    'r_side': ['right_shoulder', 'right_hip'],
    'lr_hip': ['left_hip', 'right_hip'],
    'l_forearm': ['left_elbow', 'left_wrist'],
    'r_forearm': ['right_elbow', 'right_wrist'],
    'l_arm': ['left_shoulder', 'left_elbow'],
    'r_arm': ['right_shoulder', 'right_elbow'],
    'l_thigh': ['left_hip', 'left_knee'],
    'r_thigh': ['right_hip', 'right_knee'],
    'l_calf': ['left_knee', 'left_ankle'],
    'r_calf': ['right_knee', 'right_ankle'],
}
default_angles = [
    ['lr_shoulder', 'l_side'],
    ['lr_shoulder', 'r_side'],
    ['l_side', 'lr_hip'],
    ['r_side', 'lr_hip']
]
default_ratios = [
    ['lr_shoulder', 'lr_hip'],
    ['l_side', 'r_side'],
    ['l_side', 'lr_hip'],
]
default_template = {
    'angles': default_angles,
    'ratio': default_ratios,
}

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

    def kp_vector(self, key1: str, key2: str = None):
        """
        Returns a vector between two keypoints by name.
        """
        if key2 is not None:
            return Vector(self[key1][..., :3], self[key2][..., :3])
        else:
            n1, n2 = lines[key1]
            return Vector(self[n1][..., :3], self[n2][..., :3])

    def angle(self, key1: str, key2: str = None, key3: str = None):
        if key3 is None:
            if key1 not in lines or key2 not in lines:
                raise ValueError(f'Invalid angle: {key1}')
            else:
                v1 = self.kp_vector(*lines[key1])
                v2 = self.kp_vector(*lines[key2])
                return v1.angle(v2)

    def similarity(self, other: 'Pose', template: str = '', **kwargs):
        """
        A similarity metric between two poses.
        There are many ways to implement this, depending on how we can make
        the most out different concepts of "similarity" for different cases.
        """
        if template == 'skeletal_angle':
            angles = kwargs.get('angles', None)
            if angles is None:
                raise ValueError('Must provide angles for skeletal_angle template')
            return self.skeletal_angle_similarity(other, angles)
            # NOTE: Maybe a 'body_parts' function to extract this out is better?
            pose_A = Vector([self.kp_vector(*angle).data for angle in angles])
        else:
            raise NotImplementedError

    def __repr__(self):
        return f'Pose({self.data})'
    
    def similar_to(self, p2, template=default_template, max_angle_diff=30, max_ratio_diff=1):
        for angle in template['angles']:
            a1 = self.angle(*angle)
            a2 = p2.angle(*angle)
            agl = rad_to_deg(min(abs(a1 - a2), math.pi - abs(a1 - a2)))
            if agl > max_angle_diff:
                return False
        for kp_a, kp_b in template['ratio']:
            r11 = self.kp_vector(kp_a)
            r12 = self.kp_vector(kp_b)
            r21 = p2.kp_vector(kp_a)
            r22 = p2.kp_vector(kp_b)
            ratio1 = r11.magnitude / r12.magnitude
            ratio2 = r21.magnitude / r22.magnitude
            if abs(ratio1 - ratio2) > max_ratio_diff:
                return False
        return True

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
        return Pose(self.data[slice])

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
