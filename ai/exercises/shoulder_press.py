import math

from ai.base.exercise import BatchSamplingExercise
from ai.base.vector import xaxis
from ai.exercises.utils import deg_to_rad, rad_to_deg


class ShoulderPress(BatchSamplingExercise):
    def __init__(self, window_size: int = 10,):
        super().__init__(window_size)

    def evaluation(self):
        state = self.state
        window = self.lastest_window()
        allowed_error = deg_to_rad(10)
        left_arm = window.joint_vector_series('left_wrist', 'left_elbow')
        right_arm = window.joint_vector_series('right_wrist', 'right_elbow')
        print(f"STATE: {state}")
        if state == self.prev_state and state in ['up', 'down']:
            print("judging")
            print(left_arm.pairwise_angle(xaxis).shape)
            la_xaxis_angle = left_arm.pairwise_angle(xaxis)
            ra_xaxis_angle = right_arm.pairwise_angle(xaxis)
            if abs(la_xaxis_angle.max() - math.pi/2) > allowed_error \
               or abs(ra_xaxis_angle.max() - math.pi/2) > allowed_error:
                # self.msg_queue.put('U shud keep your arms straight')
                print("gay arm")
        elif state != self.prev_state:
            bl_arm = window.joint_vector_series('left_elbow', 'left_shoulder')
            br_arm = window.joint_vector_series('right_elbow', 'right_shoulder')
            la_xaxis_angle = bl_arm.pairwise_angle(xaxis)
            ra_xaxis_angle = br_arm.pairwise_angle(xaxis)
            if abs(la_xaxis_angle.max() - math.pi/2) > allowed_error \
               or abs(ra_xaxis_angle.max() - math.pi/2) > allowed_error:
                # self.msg_queue.PUT('U shud keep your arms straight')
                print(f"harder arm, angle={rad_to_deg(bl_arm.angle(xaxis))}")

    @property
    def state(self):
        window = self.lastest_window()
        # Make this piece works again
        lw_series = window.kp_series('left_wrist')
        if lw_series.displacement[0][1] < -0.01:
            return 'up'
        elif lw_series.displacement[0][1] > 0.01:
            return 'down'
        else:
            return 'none'
