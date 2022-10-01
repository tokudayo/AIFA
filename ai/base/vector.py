from typing import Optional
import numpy as np


class Vector(object):
    """
    Represent vectors between pairs of points.
    """
    def __init__(self,
                 m1: np.ndarray,
                 m2: Optional[np.ndarray] = None,
                 name: Optional[str] = None):
        """
        Takes two matrices of points and calculates the vector between them.
        If only one matrix is given, it is assumed to be a matrix of vectors.
        """

        # Add a dimension to the data if it is 1D
        if m1.ndim < 2:
            m1 = m1[None, :]
        if m2 is not None and m2.ndim < 2:
            m2 = m2[None, :]
        # Add z dim if needed
        if m1.shape[1] == 2:
            m1 = np.hstack((m1, np.zeros((m1.shape[0], 1))))
        if m2 is not None and m2.shape[1] == 2:
            m2 = np.hstack((m2, np.zeros((m2.shape[0], 1))))
        self.data = m1 if m2 is None else m2 - m1
        self._magnitude = self.__magnitude()
        self._unit_v = self.__unit_v()
        self.name = name

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def unit_v(self):
        return self._unit_v

    def is_against(self, other: 'Vector', threshold: float = -0.5):
        """NOTE: More on this later"""
        return self.data@other.data.T < threshold

    def angle(self, other: 'Vector'):
        """
        1v1 angle calculation between two matrices of vectors.
        This assumes the `other` Vector has the same number of vectors
        as `self`.
        """
        return np.arccos((self.unit_v*other.unit_v).sum(axis=1))

    def pairwise_angle(self, other: 'Vector'):
        """
        Pairwise angle calculation between two matrices of vectors.
        Returns a MxN matrix of angles, where M is the number of vectors
        in `self` and N is the number of vectors in `other`.
        """
        return np.arccos(self.unit_v@other.unit_v.T)

    def __repr__(self) -> str:
        return f'Vector({self.name}, {self.data})'

    def __magnitude(self):
        return np.linalg.norm(self.data, axis=1)

    def __unit_v(self):
        return self.data / self.magnitude[:, None]


xaxis = Vector(np.array([[1, 0, 0]]))
yaxis = Vector(np.array([[0, 1, 0]]))
zaxis = Vector(np.array([[0, 0, 1]]))
