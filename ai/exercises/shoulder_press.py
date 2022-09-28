from typing import List, Tuple

from ai.base.exercise import Exercise


class ShoulderPress(Exercise):
    def __init__(self, memory: int = 30, window_size: int = 10):
        super().__init__(memory, window_size)

    def update(self, kps: List[Tuple[float, float, float]]):
        super().update(kps)

    def evaluation(self):
        state = self.state
        print(self.state)
        # if state == 'start':
        #     return self._start()
        # elif state == 'up':
        #     return self._up()
        # elif state == 'down':
        #     return self._down()
        # elif state == 'finish':
        #     return self._finish()

    @property
    def state(self):
        kps = self.kps
        if kps['left_wrist'].displacement[1] < -0.01:
            return 'up'
        elif kps['left_wrist'].displacement[1] > 0.01:
            return 'down'
        else:
            return 'none'
