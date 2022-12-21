import math
from typing import Optional
import numpy as np

from aifa.base.exercise import BatchSamplingExercise
from aifa.base.vector import Vector, xaxis, yaxis
from aifa.exercises.utils import deg_to_rad


def check_perpendicular_limb(limb: Vector, target: Optional['Vector'] = xaxis, allowed_error=15):
    allowed_error = deg_to_rad(allowed_error)
    limb_xaxis_angle = limb.pairwise_angle(target)
    if abs(limb_xaxis_angle.mean() - math.pi/2) > allowed_error:
        return False
    else:
        return True

class ShoulderPress(BatchSamplingExercise):
    def __init__(self, window_size: int = 10, r=0.1):
        super().__init__(window_size)
        self.r = r

    def evaluation(self, _, verbose=True):
        """
        Evaluate current state. Emits messages if fault is detected. User must fix the fault first before the next evaluation.
        Rules for this exercise:
        1. Keep the wrist to elbow part
        2. Hand must be straight when extended at the top
        3. Keep the elbow to shoulder part to the side of the body, only slightly to the front when at ready-to-lift position
        3. Keep body straight. (TBI)
        """
        state = self.state
        # window = self.lastest_window()
        msg_list = []
        # if verbose: print(f"STATE: {state}, LAST FAULT: {self.last_fault}")

        # When at the top
        if state != self.prev_state and self.prev_state == 'up':
            return 'top'
                
        # When at the bottom
        if state != self.prev_state and self.prev_state == 'down':
            return 'bottom'

        return state

    @property
    def state(self):
        window = self.lastest_window()
        # Distance from hip to shoulder
        h = (window.joint_vector_series('left_shoulder', 'left_hip').magnitude + window.joint_vector_series('right_shoulder', 'right_hip').magnitude) / 2
        h = np.sum(h) / h.shape
        k = self.r

        kps = window.kp_series('left_wrist', 'right_wrist', 'left_elbow', 'right_elbow').data
        displacement = (kps[-1] - kps[0]).mean(axis=0)[1]
        if displacement < -k * h:
            return 'up'
        elif displacement > k * h:
            return 'down'
        else:
            return 'static'
        
        
        
