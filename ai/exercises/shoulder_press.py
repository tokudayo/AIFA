import math
from typing import Optional

from ai.base.exercise import BatchSamplingExercise
from ai.base.vector import Vector, xaxis, zaxis
from ai.exercises.utils import deg_to_rad, rad_to_deg
from queue import Queue

def check_perpendicular_limb(window, target: Optional['Vector'] = xaxis, limb = "wrist_elbow", side = "left", allowed_error=0.26):
    if limb == "wrist_elbow":
        if side == "left":
            limb = window.joint_vector_series('left_wrist', 'left_elbow')
        elif side == "right":
            limb = window.joint_vector_series('right_wrist', 'right_elbow')

    if limb == "elbow_shoulder":
        if side == "left":
            limb = window.joint_vector_series('left_elbow', 'left_shoulder')
        elif side == "right":
            limb = window.joint_vector_series('right_elbow', 'right_shoulder')
    
    if target is None:
        limb_xaxis_angle = limb.pairwise_angle(xaxis)
    else:
        limb_xaxis_angle = limb.pairwise_angle(target)

    if abs(limb_xaxis_angle.max() - math.pi/2) > allowed_error:
        return False
    else:
        return True


class ShoulderPress(BatchSamplingExercise):
    def __init__(self, window_size: int = 10,):
        super().__init__(window_size)

    def evaluation(self, verbose=True):
        """
        Evaluate current state. Emits messages if fault is detected. User must fix the fault first before the next evaluation.
        Rules for this exercise:
        1. Keep the wrist to elbow part perpendicular to the ground while moving
        2. Hand must be straight when extended at the top
        3. Keep the elbow to shoulder part to the side of the body, only slightly to the front when at ready-to-lift position
        3. Keep body straight. (TBI)
        """
        state = self.state
        window = self.lastest_window()
        allowed_error = deg_to_rad(15)
        msg_list = []
        if verbose: print(f"STATE: {state}, LAST FAULT: {self.last_fault}")
        # When moving
        if state == self.prev_state and state in ['up', 'down'] or self.last_fault is None:
            # Keep the wrist to elbow part perpendicular to the ground while moving
            if not check_perpendicular_limb(window, limb = "wrist_elbow", side = "left", allowed_error=allowed_error):
                msg_list.append("Upper left arm must be straight.")
            if not check_perpendicular_limb(window, limb = "wrist_elbow", side = "right", allowed_error=allowed_error):
                msg_list.append("Upper right arm must be straight.")

        # When at the top
        if state != self.prev_state and self.prev_state == 'up' or self.last_fault == "top":
            if self.last_fault != "top" and verbose: print("At the top.")
            # Keep the elbow to shoulder part to the side, but slightly to the front
            if not check_perpendicular_limb(window, limb = "elbow_shoulder", side = "left", allowed_error=allowed_error):
                msg_list.append("Extend your left arm fully at the top.")
                self.last_fault = 'top'
            elif not check_perpendicular_limb(window, limb = "elbow_shoulder", side = "right", allowed_error=allowed_error):
                msg_list.append("Extend your right arm fully at the top.")
                self.last_fault = 'top'
            else:
                self.last_fault = None
                
        # When at the bottom
        elif state != self.prev_state and self.prev_state == 'down':
            if verbose: print("At the bottom.")
        # Keep the elbow to shoulder part to the side, only slightly to the front
        # TBI
        return msg_list

    @property
    def state(self):
        window = self.lastest_window()
        lw_series = window.kp_series('left_wrist')
        rw_series = window.kp_series('right_wrist')
        # detect the state
        if lw_series.displacement[0][1] < -0.05:
            return 'up'
        elif lw_series.displacement[0][1] > 0.05:
            return 'down'
        else:
            return 'none'
        
