import pickle

from aifa.base.pose import Pose, PoseSeries
from aifa.experimental.state import StateSeries

class Exercise():
    def __init__(self):
        self.series = PoseSeries()

    def update(self, pose: Pose):
        """Pass normalized keypoints info in and update internal state"""
        self.series.update(pose)

    def evaluation(self, window: PoseSeries):
        """Evaluate current state. Emits messages to the queue if needed."""
        raise NotImplementedError

    @property
    def state(self):
        raise NotImplementedError


class BatchSamplingExercise(Exercise):
    def __init__(self, window_size: int = 10, state_series_length: int = 5, default_pose: Pose = './data/pose.np'):
        super().__init__()
        self.window_size = window_size
        self.prev_state = None
        self.stateSeries = StateSeries(length = state_series_length)
        self.direction = 'static'
        self.prev_direction = 'static'
        self.last_fault = None
        self.window = None
        self.default_pose = pickle.load(open(default_pose, 'rb'))

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
        if len(self.series.data) % self.window_size == 0 and len(self.series.data) > 0:
            window = self.lastest_window()
            filtered_window = []
            for i in range(self.window_size):
                p = Pose(window[i])
                if p.similar_to(self.default_pose):
                    filtered_window.append(p)
            if len(filtered_window) <= int(self.window_size * 0.5):
                return "Errornous pose detected."
            result = self.evaluation(PoseSeries(filtered_window))
            # result = self.evaluation(window)
            self.prev_state = self.state
            self.prev_window = self.window
            # Experimental
            self.prev_direction = self.stateSeries.max()
            self.stateSeries.update(self.state)
            return result
