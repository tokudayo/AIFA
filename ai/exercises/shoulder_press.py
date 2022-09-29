import math
from typing import List, Tuple

from ai.base.exercise import Exercise
from ai.base.vector import xaxis
from ai.exercises.utils import deg_to_rad, rad_to_deg


class ShoulderPress(Exercise):
    def __init__(self,
                 memory: int = 30,
                 window_size: int = 6,
                 msg_queue_size: int = 10):
        super().__init__(memory, window_size, msg_queue_size)

    def update(self, kps: List[Tuple[float, float, float]]):
        super().update(kps)

    def evaluation(self):
        state = self.state
        # print(
        #     f"Current state: {self.state}, previous state: {self.prev_state}"
        # )
        # 4 cases:
        allowed_error = deg_to_rad(10*2)
        left_arm = self.joint_vector('left_wrist', 'left_elbow')
        right_arm = self.joint_vector('right_wrist', 'right_elbow')
        print(f"STATE: {state}")
        if state == self.prev_state and state in ['up', 'down']:
            print("judging")
            if abs(left_arm.angle(xaxis) - math.pi/2) > allowed_error or abs(
                    right_arm.angle(xaxis) - math.pi/2) > allowed_error:
                # self.msg_queue.put('U shud keep your arms straight')
                print("gay arm")
        elif state != self.prev_state:
            bl_arm = self.joint_vector('left_elbow', 'left_shoulder')
            br_arm = self.joint_vector('right_elbow', 'right_shoulder')
            if abs(bl_arm.angle(xaxis) - math.pi/2) > allowed_error or abs(
                    br_arm.angle(xaxis) - math.pi/2) > allowed_error:
                # self.msg_queue.put('U shud keep your arms straight')
                print(f"harder arm, angle={rad_to_deg(bl_arm.angle(xaxis))}")

    @property
    def state(self):
        kps = self.kps
        if kps['left_wrist'].displacement[1] < -0.01:
            return 'up'
        elif kps['left_wrist'].displacement[1] > 0.01:
            return 'down'
        else:
            return 'none'
