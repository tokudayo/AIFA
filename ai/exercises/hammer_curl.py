import math
from typing import Optional
import numpy as np

from ai.base.exercise import BatchSamplingExercise
from ai.base.vector import Vector, xaxis, yaxis
from ai.exercises.utils import deg_to_rad, rad_to_deg


def check_perpendicular_limb(limb: Vector, target: Optional['Vector'] = xaxis, allowed_error=15):
    allowed_error = deg_to_rad(allowed_error)
    limb_xaxis_angle = limb.pairwise_angle(target)
    if abs(limb_xaxis_angle.mean() - math.pi/2) > allowed_error:
        return False
    else:
        return True


class HammerCurl(BatchSamplingExercise):
    def __init__(self, window_size: int = 10,):
        super().__init__(window_size)
        self.lstates = []
        self.rstates = []

    def evaluation(self, verbose=True):
        state = self.state
        window = self.lastest_window()
        msg_list = []
        # if verbose: print(f"STATE: {state}")

        # # check if body is straight
        # left_upright = window.joint_vector_series('left_shoulder', 'left_hip')
        # right_upright = window.joint_vector_series('right_shoulder', 'right_hip')
        # if not check_perpendicular_limb(left_upright, xaxis, allowed_error=10.):
        #     msg_list.append("Keep your left side straight")
        # if not check_perpendicular_limb(right_upright, xaxis, allowed_error=10.):
        #     msg_list.append("Keep your right side straight")
        
        la_arm = window.joint_vector_series('left_shoulder', 'left_elbow')
        ra_arm = window.joint_vector_series('right_shoulder', 'right_elbow')
        if not check_perpendicular_limb(limb = la_arm, allowed_error=20.):
            msg_list.append("Upper left arm must be straight.")
        if not check_perpendicular_limb(limb = ra_arm, allowed_error=20.):
            msg_list.append("Upper right arm must be straight.")

        # When at the top
        if state != self.prev_state and self.prev_state == 'up':
            left_forearm =  window.joint_vector_series('left_elbow', 'left_wrist')
            right_forearm =  window.joint_vector_series('right_elbow', 'right_wrist')
            left_arm = window.joint_vector_series('left_elbow', 'left_shoulder')
            right_arm = window.joint_vector_series('right_elbow', 'right_shoulder')

            if left_forearm.angle(left_arm).min() > deg_to_rad(45.):
                msg_list.append("L Problem")
            
            if right_forearm.angle(right_arm).min() > deg_to_rad(45.):
                msg_list.append("R Problem")
                
        # When at the bottom
        if state != self.prev_state and self.prev_state == 'down':
            left_forearm =  window.joint_vector_series('left_elbow', 'left_wrist')
            right_forearm =  window.joint_vector_series('right_elbow', 'right_wrist')
            if not check_perpendicular_limb(limb = left_forearm, target = xaxis, allowed_error=10.):
                msg_list.append("Problem.")
            if not check_perpendicular_limb(limb = right_forearm, target = xaxis, allowed_error=10.):
                msg_list.append("Problem.")
        return msg_list

    @property
    def state(self):
        window = self.lastest_window()
        # Distance from hip to shoulder
        h = (window.joint_vector_series('left_shoulder', 'left_hip').magnitude + window.joint_vector_series('right_shoulder', 'right_hip').magnitude) / 2
        h = np.sum(h) / h.shape
        k = 0.05

        kps = window.kp_series('left_wrist', 'right_wrist').data
        displacement = (kps[-1] - kps[0]).mean(axis=0)[1]
        if displacement < -k * h:
            return 'up'
        elif displacement > k * h:
            return 'down'
        else:
            return 'static'
