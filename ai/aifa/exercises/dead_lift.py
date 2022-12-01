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
        torso = window.joint_vector_series('left_shoulder', 'left_hip').add(window.joint_vector_series('right_shoulder', 'right_hip'))
        if not check_perpendicular_limb(torso, xaxis, allowed_error=10.):
            msg_list.append("Keep your torso straight.")


        # Straight leg check - might be rudundant, removed for now
        # left_leg = window.joint_vector_series('left_ankle', 'left_knee')
        # right_leg = window.joint_vector_series('right_ankle', 'right_knee')
        # if not check_perpendicular_limb(left_leg, xaxis, allowed_error=15.):
        #     msg_list.append("Keep your left leg straight.")
        # if not check_perpendicular_limb(right_leg, xaxis, allowed_error=15.):
        #     msg_list.append("Keep your right leg straight.")
        
        # Stance check
        hip_length = window.joint_vector_series('left_hip', 'right_hip').magnitude.mean()
        ankle_length = window.joint_vector_series('left_ankle', 'right_ankle').magnitude.mean()
        if ankle_length > hip_length*2.35:
            msg_list.append("Keep your legs closer together.")
        elif ankle_length < hip_length:
            msg_list.append("Keep your legs wider apart.")
        
        # Grip check
        shoulder_width = window.joint_vector_series('left_shoulder', 'right_shoulder').magnitude.mean()
        grip_width = window.joint_vector_series('left_wrist', 'right_wrist').magnitude.mean()
        if grip_width > shoulder_width*1.85:
            msg_list.append("Keep your grip closer together.")
        elif grip_width < shoulder_width*1.1:
            msg_list.append("Keep your grip wider apart.")
        
        # Check if squatting/sitting
        hips = window.kp_series('left_hip', 'right_hip').data
        knees = window.kp_series('left_knee', 'right_knee').data
        h = (window.joint_vector_series('left_ankle', 'left_knee').magnitude + window.joint_vector_series('right_ankle', 'right_knee').magnitude) / 2
        h = np.sum(h) / h.shape
        margin = h * 0.25
        #print((hips[-1, :, 1] >= knees[-1, :, 1] - margin).any())
        if (hips[-1, :, 1] >= knees[-1, :, 1] - margin).any():
            msg_list.append("Don't drop hip down too much.")
        
        # Check if hand is somewhat straight
        # To be optimized later, code is a bit messy but it works
        left_shoulder_to_wrist = window.joint_vector_series('left_wrist', 'left_shoulder')
        right_shoulder_to_wrist = window.joint_vector_series('right_wrist', 'right_shoulder')
        left_shoulder_to_elbow = window.joint_vector_series('left_elbow', 'left_shoulder')
        right_shoulder_to_elbow = window.joint_vector_series('right_elbow', 'right_shoulder')
        # check angle between shoulder to wrist and shoulder to elbow
        if left_shoulder_to_wrist.angle(left_shoulder_to_elbow).min() > deg_to_rad(15):
            msg_list.append("Keep your left hand straight.")
        if right_shoulder_to_wrist.angle(right_shoulder_to_elbow).min() > deg_to_rad(15):
            msg_list.append("Keep your right hand straight.")

        return ' '.join(msg_list)

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
        
