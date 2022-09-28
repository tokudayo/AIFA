import numpy as np
from numpy.linalg import norm

from ai.base.keypoint import KeyPoint


class Vector(object):
    '''
    Vector class for calculating the vector between two keypoints
    '''
    def __init__(self, kp1: KeyPoint, kp2: KeyPoint):
        self.vector = np.array(kp2.pos[0] - kp1.pos[0])
        self.name = f'{kp1.name}-{kp2.name}, {self.vector}'

    def angle(self, other: 'Vector'):
        return np.arccos(
            self.vector @ other.vector / (norm(self.vector)*norm(other.vector))
        )

    def magnitude(self):
        return norm(self.vector)

    def is_against(self, other: 'Vector', threshold: float = -0.5):
        return self.vector@other.vector < threshold

    def direction(self):
        return self.vector / self.magnitude()

    def __repr__(self) -> str:
        return f'Vector({self.name})'


xaxis = Vector(
    KeyPoint('origin', 0, 0), KeyPoint('x-axis', 1, 0)
)
yaxis = Vector(
    KeyPoint('origin', 0, 0), KeyPoint('y-axis', 0, 1)
)
