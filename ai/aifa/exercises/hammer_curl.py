import math
from typing import Optional
import numpy as np

from aifa.base.exercise import BatchSamplingExercise
from aifa.base.vector import Vector, xaxis, yaxis
from aifa.exercises.utils import deg_to_rad, rad_to_deg


def is_perpendicular(vec1: Vector, vec2: Vector, allowed_error=15.):
    allowed_error = deg_to_rad(allowed_error)
    pw_angle = vec1.pairwise_angle(vec2)
    if abs(pw_angle.mean() - math.pi/2) > allowed_error:
        return False
    else:
        return True


class HammerCurl(BatchSamplingExercise):
    def __init__(self,
                 window_size: int = 10,
                 movement_threshold: float = 0.07,
                 straight_arm_threshold: float = 30.,
                 elbow_angle_threshold: float = 80.,):
        super().__init__(window_size)
        self.prev_state = 'static'
        self.movement_threshold = movement_threshold
        self.straight_arm_threshold = straight_arm_threshold
        self.elbow_angle_threshold = elbow_angle_threshold

    def _decode_state(self, state):
        lstate = 'static' if state[0] != 'l' else state[2:]
        rstate = 'static' if state[0] != 'r' else state[2:]
        return lstate, rstate

    def evaluation(self, verbose=True):
        window = self.lastest_window()
        msg_list = []
        # if verbose: print(f"STATE: {self.state}, P_STATE: {self.prev_state}")

        # check if body is straight
        left_upright = window.joint_vector_series('left_shoulder', 'right_shoulder')
        right_upright = window.joint_vector_series('left_hip', 'right_hip')
        if not is_perpendicular(left_upright, yaxis, allowed_error=10.):
            msg_list.append("Keep your left side straight")
        if not is_perpendicular(right_upright, yaxis, allowed_error=10.):
            msg_list.append("Keep your right side straight")
        
        la_arm = window.joint_vector_series('left_shoulder', 'left_elbow')
        ra_arm = window.joint_vector_series('right_shoulder', 'right_elbow')
        if not is_perpendicular(la_arm, xaxis, allowed_error=self.straight_arm_threshold):
            msg_list.append("Upper left arm must be straight.")
        if not is_perpendicular(ra_arm, xaxis, allowed_error=self.straight_arm_threshold):
            msg_list.append("Upper right arm must be straight.")

        lstate, rstate = self._decode_state(self.state)
        pr_lstate, pr_rstate = self._decode_state(self.prev_state)
        # print(f"lstate: {lstate}, rstate: {rstate}, pr_lstate: {pr_lstate}, pr_rstate: {pr_rstate}")

        # When at the top
        if lstate != pr_lstate and pr_lstate == 'up':
            left_forearm =  window.joint_vector_series('left_elbow', 'left_wrist')
            left_arm = window.joint_vector_series('left_elbow', 'left_shoulder')
            if left_forearm.angle(left_arm).min() > deg_to_rad(self.elbow_angle_threshold):
                msg_list.append("Curl your left arm further.")

        if rstate != pr_rstate and pr_rstate == 'up':
            right_forearm =  window.joint_vector_series('right_elbow', 'right_wrist')
            right_arm = window.joint_vector_series('right_elbow', 'right_shoulder')
            if right_forearm.angle(right_arm).min() > deg_to_rad(self.elbow_angle_threshold):
                msg_list.append("Curl your right arm further.")
                
        # When at the bottom
        if lstate != pr_lstate and pr_lstate == 'down':
            left_forearm =  window.joint_vector_series('left_elbow', 'left_wrist')
            if not is_perpendicular(left_forearm, xaxis, allowed_error=self.straight_arm_threshold):
                msg_list.append("Bring the weights on your left hand down fully.")

        if rstate != pr_rstate and pr_rstate == 'down':
            right_forearm =  window.joint_vector_series('right_elbow', 'right_wrist')
            if not is_perpendicular(right_forearm, xaxis, allowed_error=self.straight_arm_threshold):
                msg_list.append("Bring the weights on your left hand down fully.")
        return ' '.join(msg_list)

    @property
    def state(self):
        window = self.lastest_window()
        # Distance from hip to shoulder
        hip_length = (
            ( window.joint_vector_series('left_shoulder', 'left_hip').magnitude
            + window.joint_vector_series('right_shoulder', 'right_hip').magnitude) / 2
        ).mean()
        thres = self.movement_threshold * hip_length

        kps = window.kp_series('left_wrist', 'right_wrist').data
        displacement = (kps[-1] - kps[0])
        ldis = displacement[0][1]
        rdis = displacement[1][1]
        state = 'static'
        if abs(ldis) > abs(rdis):
            if ldis < -thres:
                state = 'l_up'
            elif ldis > thres:
                state = 'l_down'
        else:
            if rdis < -thres:
                state = 'r_up'
            elif rdis > thres:
                state = 'r_down'
        return state