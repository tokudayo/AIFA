from threading import Thread

import cv2
from aifa.base.pose import Pose

from aifa.utils import Timer
from aifa.inputs import Cv2VideoStream, Cv2WebcamStream
from aifa.models import BlazePose
from aifa.exercises import ShoulderPress, HammerCurl, DeadLift


class AIFlow(object):
    def __init__(self, count: int = 1):
        self.input = Cv2VideoStream(f"videos/clip_hc/o4_{count}.avi", max_size=720, max_queue_size=1)
        # self.input = Cv2VideoStream("videos/hc/s1.mp4", max_size=720)
        # self.input = Cv2WebcamStream()
        # self.model = DummyHpeModel()
        self.model = BlazePose(complexity=1, static_mode=False)
        # Experimental
        #self.evaluator = exp_ShoulderPress()
        self.evaluator = ShoulderPress()

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        self.input.start()
        cnt = 0
        while not self.input.stopped:
            frame = self.input.get_frame()
            if frame is None:
                continue
            cnt += 1
            h, w, _ = frame.shape
            # frame = cv2.flip(frame, 0)
            keypoints = self.model(frame)
            drawn = self.model.draw(frame, keypoints)
            if keypoints is None:
                continue

            kps = self.model.postprocess(keypoints.landmark)

            results = self.evaluator.update(Pose(kps, w, h))
            # check if the list returned is empty
            if results: print(results)
            # flip horizontally
            # drawn = cv2.flip(drawn, 1)
            
            cv2.imshow("funny", drawn)
            if cv2.waitKey(1) == ord('q'):
                self.input.stop()
                break

        cv2.destroyAllWindows()
        print(f"total frames: {cnt}")

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1])
    timer = Timer()
    timer.start()
    flow = AIFlow(count=count)
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
