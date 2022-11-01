import math
from typing import Optional

from ai.base.exercise import BatchSamplingExercise
from ai.base.vector import Vector, xaxis, yaxis, zaxis
from ai.exercises.utils import deg_to_rad, rad_to_deg
from queue import Queue
import numpy as np
def check_perpendicular_limb(limb: Vector, target: Optional['Vector'] = xaxis, allowed_error=0.26):
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
        1. Keep the wrist to elbow part
        2. Hand must be straight when extended at the top
        3. Keep the elbow to shoulder part to the side of the body, only slightly to the front when at ready-to-lift position
        3. Keep body straight. (TBI)
        """
        state = self.state
        window = self.lastest_window()
        allowed_error = deg_to_rad(15)
        msg_list = []
        if verbose: print(f"STATE: {state}, LAST FAULT: {self.last_fault}")

        # check if body is straight
        left_upright = window.joint_vector_series('left_shoulder', 'left_hip')
        right_upright = window.joint_vector_series('right_shoulder', 'right_hip')
        if not check_perpendicular_limb(left_upright, xaxis, allowed_error=allowed_error):
            msg_list.append("Keep your left side straight")
        if not check_perpendicular_limb(right_upright, xaxis, allowed_error=allowed_error):
            msg_list.append("Keep your right side straight")
        
        # When moving
        if state == self.prev_state and state in ['up', 'down'] or self.last_fault is None:
            # Keep the wrist to elbow part perpendicular to the ground while moving
            la_arm = window.joint_vector_series('left_wrist', 'left_elbow')
            ra_arm = window.joint_vector_series('right_wrist', 'right_elbow')
            if not check_perpendicular_limb(limb = la_arm, allowed_error=allowed_error):
                msg_list.append("Upper left arm must be straight.")
            if not check_perpendicular_limb(limb = ra_arm, allowed_error=allowed_error):
                msg_list.append("Upper right arm must be straight.")

        # When at the top
        if state != self.prev_state and self.prev_state == 'up' and state in ['up','static'] or self.last_fault == "top":
            #if self.last_fault != "top" and verbose: print("At the top.")
            lb_arm =  window.joint_vector_series('left_elbow', 'left_shoulder')
            rb_arm =  window.joint_vector_series('right_elbow', 'right_shoulder')
            # Keep the elbow to shoulder part to the side, but slightly to the front
            if not check_perpendicular_limb(limb = lb_arm, allowed_error=allowed_error):
                msg_list.append("Extend your left arm fully at the top.")
                self.last_fault = 'top'
            elif not check_perpendicular_limb(limb = rb_arm, allowed_error=allowed_error):
                msg_list.append("Extend your right arm fully at the top.")
                self.last_fault = 'top'
            else:
                self.last_fault = None
                
        # When at the bottom
        if state != self.prev_state and self.prev_state == 'down' and state in ['down','static'] or self.last_fault == "bottom":
            #if verbose: print("At the bottom.")
        # Keep the elbow to shoulder part to the side, only slightly to the front
            lb_arm =  window.joint_vector_series('left_elbow', 'left_shoulder')
            rb_arm =  window.joint_vector_series('right_elbow', 'right_shoulder')
            if not check_perpendicular_limb(limb = lb_arm, target = yaxis, allowed_error=allowed_error):
                msg_list.append("Keep your left arm to the side.")
                self.last_fault = 'bottom'
            if not check_perpendicular_limb(limb = rb_arm, target = yaxis, allowed_error=allowed_error):
                msg_list.append("Keep your right arm to the side.")
                self.last_fault = 'bottom'
        return msg_list

    @property
    def state(self):
        window = self.lastest_window()
        # Distance from hip to shoulder
        h = (window.joint_vector_series('left_shoulder', 'left_hip').magnitude + window.joint_vector_series('right_shoulder', 'right_hip').magnitude) / 2
        h = np.sum(h) / h.shape
        k = 0.01
        # Suppose arm is from wrist to elbow
        la_arm = window.joint_vector_series('left_wrist', 'left_elbow')
        ra_arm = window.joint_vector_series('right_wrist', 'right_elbow')
        

        # find if both arm moved up or down
        if (la_arm.data[-1] - la_arm.data[0])[1] > k * h and (ra_arm.data[-1] - ra_arm.data[0])[1] > k * h:
            return 'up'
        elif (la_arm.data[-1] - la_arm.data[0])[1] < -k * h and (ra_arm.data[-1] - ra_arm.data[0])[1] < -k * h:
            return 'down'
        else:
            return 'static'
        
        
