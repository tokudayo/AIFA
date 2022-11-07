import math
from typing import Optional
import numpy as np

from ai.base.exercise import BatchSamplingExercise
from ai.base.vector import Vector, xaxis, yaxis
from ai.exercises.utils import deg_to_rad


def check_perpendicular_limb(limb: Vector, target: Optional['Vector'] = xaxis, allowed_error=15):
    allowed_error = deg_to_rad(allowed_error)
    limb_xaxis_angle = limb.pairwise_angle(target)
    if abs(limb_xaxis_angle.mean() - math.pi/2) > allowed_error:
        return False
    else:
        return True


class DeadLift(BatchSamplingExercise):
    def __init__(self, window_size: int = 10,):
        super().__init__(window_size)

    def evaluation(self, verbose=True):
        """
        Evaluate current state. Emits messages if fault is detected. User must fix the fault first before the next evaluation.
        Rules for this exercise:
        1, Check if body is straight
        2. Ensure legs width must not be too wide or too narrow
        3. Grip the bar with a shoulder width grip
        4. When going down, make sure not 'sitting'
        """
        state = self.state
        state_series = self.stateSeries
        window = self.lastest_window()
        msg_list = []
        if verbose: print(f"STATE: {state}, LAST FAULT: {self.last_fault}")
        # check if body is straight
        left_upright = window.joint_vector_series('left_shoulder', 'left_hip')
        right_upright = window.joint_vector_series('right_shoulder', 'right_hip')
        if not check_perpendicular_limb(left_upright, xaxis, allowed_error=10.):
            msg_list.append("Keep your left side straight")
        if not check_perpendicular_limb(right_upright, xaxis, allowed_error=10.):
            msg_list.append("Keep your right side straight")

        # check if legs are straight with the ground 
        left_leg = window.joint_vector_series('left_ankle', 'left_knee')
        right_leg = window.joint_vector_series('right_ankle', 'right_knee')
        if not check_perpendicular_limb(left_leg, xaxis, allowed_error=10.):
            msg_list.append("Keep your left leg straight.")
        if not check_perpendicular_limb(right_leg, xaxis, allowed_error=10.):
            msg_list.append("Keep your right leg straight.")
        
        # check if legs are too wide or too narrow
        hip_length = window.joint_vector_series('left_hip', 'right_hip').magnitude.mean()
        ankle_length = window.joint_vector_series('left_ankle', 'right_ankle').magnitude.mean()
        if ankle_length > hip_length:
            msg_list.append("Keep your legs closer together.")
        elif ankle_length < hip_length/2:
            msg_list.append("Keep your legs wider apart.")
        
        # check if grip is too wide or too narrow
        shoulder_width = window.joint_vector_series('left_shoulder', 'right_shoulder').magnitude.mean()
        grip_width = window.joint_vector_series('left_wrist', 'right_wrist').magnitude.mean()
        if grip_width > shoulder_width:
            msg_list.append("Keep your grip closer together.")
        elif grip_width < shoulder_width/2:
            msg_list.append("Keep your grip wider apart.")
        
        # Check if squatting/sitting - In this case, we are checking if the hip to knee vector is "visible"
        # To be implemented.
        
        # Check if hand is somewhat straight
        # Might be redundant (more on this later)
        left_hand = window.joint_vector_series('left_wrist', 'left_elbow')
        right_hand = window.joint_vector_series('right_wrist', 'right_elbow')
        if not check_perpendicular_limb(left_hand, xaxis, allowed_error=10.):
            msg_list.append("Keep your left hand straight.")
        if not check_perpendicular_limb(right_hand, xaxis, allowed_error=10.):
            msg_list.append("Keep your right hand straight.")

        return msg_list

    @property
    def state(self):
        window = self.lastest_window()
        # Distance from hip to shoulder
        h = (window.joint_vector_series('left_ankle', 'left_knee').magnitude + window.joint_vector_series('right_ankle', 'right_knee').magnitude) / 2
        h = np.sum(h) / h.shape
        k = 0.1

        kps = window.kp_series('left_wrist', 'right_wrist', 'left_elbow', 'right_elbow').data
        displacement = (kps[-1] - kps[0]).mean(axis=0)[1]
        if displacement < -k * h:
            return 'up'
        elif displacement > k * h:
            return 'down'
        else:
            return 'static'
        
