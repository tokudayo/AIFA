import math
from typing import List, Tuple

from ai.base.exercise import Exercise
from ai.base.vector import xaxis


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
        error = 0.15
        left_arm = self.joint_vector('left_wrist', 'left_elbow')
        right_arm = self.joint_vector('right_wrist', 'right_elbow')
        if state == 'down' and self.prev_state == 'up':
            pass
        elif state == 'up' and self.prev_state == 'down':
            pass
        elif state == self.prev_state and state in ['up', 'down']:
            print("judging")
            if abs(left_arm.angle(xaxis) - math.pi/2) > error or abs(
                    right_arm.angle(xaxis) - math.pi/2) > error:
                # self.msg_queue.put('U shud keep your arms straight')
                print("gay arm")

    @property
    def state(self):
        kps = self.kps
        if kps['left_wrist'].displacement[1] < -0.01:
            return 'up'
        elif kps['left_wrist'].displacement[1] > 0.01:
            return 'down'
        else:
            return 'none'
