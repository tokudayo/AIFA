import yaml
import numpy as np
from ai.base.keypoint import KeyPoint

class Vector(object):
    '''
    Vector class for calculating the vector between two keypoints
    '''

    def __init__(self, Kp1: KeyPoint, Kp2: KeyPoint):
        self.vector = np.array([Kp1.pos[0][0] - Kp2.pos[0][0], Kp1.pos[0][1] - Kp2.pos[0][1], Kp1.pos[0][2] - Kp2.pos[0][2]])
        self.name = f'{self.anno[Kp1.name]}-{self.anno[Kp2.name]}'
    
    def __init__(self, kps: dict, name1, name2):
        try:
            self.vector = np.array([kps[name1].pos[0][0] - kps[name2].pos[0][0], kps[name1].pos[0][1] - kps[name2].pos[0][1], kps[name1].pos[0][2] - kps[name2].pos[0][2]])
        except KeyError:
            print(f'KeyError: {name1} or {name2} doesn\'t exist.')
        self.name = f'{name1}-{name2}'

    def __init__(self, coords1: np.ndarray, coords2: np.ndarray):
        self.vector = np.array([coords1[0] - coords2[0], coords1[1] - coords2[1], coords1[2] - coords2[2]])
        self.name = f'{coords1}-{coords2}'

    def angle(self, other: 'Vector'):
        return np.arccos(np.dot(self.vector, other.vector) / (np.linalg.norm(self.vector) * np.linalg.norm(other.vector)))
    
    def magnitude(self):
        return np.linalg.norm(self.vector)
    
    def is_against(self, other: 'Vector'):
        raise NotImplementedError

    def direction(self):
        return self.vector / self.magnitude()
    


    def __repr__(self) -> str:
        return f'Vector({self.name})'
