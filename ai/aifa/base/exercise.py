from aifa.base.pose import Pose, PoseSeries
from aifa.experimental.state import StateSeries

class Exercise():
    def __init__(self):
        self.series = PoseSeries()

    def update(self, pose: Pose):
        """Pass normalized keypoints info in and update internal state"""
        self.series.update(pose)

    def evaluation(self):
        """Evaluate current state. Emits messages to the queue if needed."""
        raise NotImplementedError

    @property
    def state(self):
        raise NotImplementedError


class BatchSamplingExercise(Exercise):
    def __init__(self, window_size: int = 10, state_series_length: int = 5,):
        super().__init__()
        self.window_size = window_size
        self.prev_state = None
        self.stateSeries = StateSeries(length = state_series_length)
        self.direction = 'static'
        self.prev_direction = 'static'
        self.last_fault = None
        self.window = None

    def lastest_window(self):
        """
        NOTE: Not the actual latest 'window'.
        Maybe we will come back to this later
        """
        return PoseSeries(
            self.series.data[-self.window_size:]
        )

    def update(self, pose: Pose):
        super().update(pose)
        if len(self.series.data) % self.window_size == self.window_size - 1:
            result = self.evaluation()
            self.prev_state = self.state
            # Experimental
            self.prev_direction = self.stateSeries.max()
            self.stateSeries.update(self.state)
            self.prev_window = self.window
            return result
