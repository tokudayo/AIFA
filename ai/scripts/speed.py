from threading import Thread
import time

import cv2
from aifa.base.pose import Pose

from aifa.utils import Timer
from aifa.inputs import Cv2VideoStream, Cv2WebcamStream
from aifa.models import BlazePose, DummyHpeModel
from aifa.exercises import ShoulderPress, HammerCurl, DeadLift


class AIFlow(object):
    def __init__(self, count: int = 1):
        self.input = Cv2VideoStream(f"./data/hc/s1.mp4", max_size=720, max_queue_size=0)
        # self.model = DummyHpeModel()
        self.model = BlazePose(complexity=1, static_mode=False)
        self.evaluator = ShoulderPress()

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        self.input.start()
        cnt = 0
        while True:
            if not self.input.stopped:
                time.sleep(0.1)
                continue
            else:
                break
        print(f"Eval start, q_size {self.input.queue.qsize()}")
        timer = Timer()
        timer.start()
        while True:
            frame = self.input.get_frame()
            if frame is None:
                break
            cnt += 1
            h, w, _ = frame.shape
            # frame = cv2.flip(frame, 0)
            keypoints = self.model(frame)
            # drawn = self.model.draw(frame, keypoints)
            if keypoints is None:
                continue

            kps = self.model.postprocess(keypoints.landmark)
            # kps = keypoints

            results = self.evaluator.update(Pose(kps, w, h))
            # check if the list returned is empty
            if results: print(results)
            # flip horizontally
            # drawn = cv2.flip(drawn, 1)
            
            # cv2.imshow("funny", drawn)
            # if cv2.waitKey(1) == ord('q'):
            #     self.input.stop()
            #     break
        timer.stop()
        print(f"Flow elapsed: {timer.elapsed:.2f}s")
        # cv2.destroyAllWindows()
        print(f"total frames: {cnt}")

if __name__ == "__main__":
    import sys
    timer = Timer()
    timer.start()
    flow = AIFlow()
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
