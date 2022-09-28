from threading import Thread

import cv2

from utils import Timer
from ai.inputs import Cv2VideoStream, Cv2WebcamStream
from ai.models import BlazePose
from ai.exercises import ShoulderPress


class AIFlow(object):
    def __init__(self):
        # self.input = Cv2VideoStream("sample.mp4")
        self.input = Cv2WebcamStream()
        # self.model = DummyHpeModel()
        self.model = BlazePose(complexity=1, static_mode=False)
        self.evaluator = ShoulderPress()
        self.exercise = None

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        self.input.start()
        while not self.input.stopped:
            frame = self.input.get_frame()
            if frame is None:
                continue
            keypoints = self.model(frame)
            drawn = self.model.draw(frame, keypoints)
            if keypoints is None:
                continue

            results = self.model.postprocess(keypoints.landmark)

            self.evaluator.update(results)

            cv2.imshow("funny", drawn)
            if cv2.waitKey(1) == ord('q'):
                self.input.stop()
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    flow = AIFlow()
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
