from typing import Optional

import numpy as np


class KeyPoint(object):
    def __init__(self,
                 name: Optional[str] = None,
                 x: float = 0.,
                 y: float = 0.,
                 z: float = 0.,
                 memory: int = 5):
        self.name = name
        self.memory = memory
        self.pos = np.zeros((memory, 3))
        self.pos[0] = np.array([x, y, z])

    def update(self, x: float, y: float, z: float):
        self.pos = np.roll(self.pos, 1, axis=0)
        self.pos[0] = np.array([x, y, z])

    @property
    def position(self):
        return self.pos[0]

    @property
    def velocity(self):
        return self.pos[0] - self.pos[1]

    @property
    def avg_velocity(self):
        return np.mean(self.pos[:-1] - self.pos[1:], axis=0)

    @property
    def acceleration(self):
        return self.velocity - self.avg_velocity

    @property
    def avg_acceleration(self):
        return np.mean(self.pos[2:] - 2*self.pos[1:-1] + self.pos[:-2], axis=0)
