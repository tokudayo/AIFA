import pickle
from threading import Thread

import cv2
from aifa.base.pose import Pose

from aifa.utils import Timer
from aifa.inputs import Cv2WebcamStream
from aifa.models import BlazePose

class AIFlow(object):
    def __init__(self):
        self.input = Cv2WebcamStream()
        self.model = BlazePose(complexity=1, static_mode=False)

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        self.input.start()
        cnt = 300
        while not self.input.stopped:
            print(cnt)
            cnt -= 1
            frame = self.input.get_frame()
            if frame is None:
                continue
            h, w, _ = frame.shape
            # frame = cv2.flip(frame, 0)
            keypoints = self.model(frame)
            drawn = self.model.draw(frame, keypoints)
            if keypoints is None:
                continue

            kps = self.model.postprocess(keypoints.landmark)
            # flip horizontally
            # drawn = cv2.flip(drawn, 1)
            
            cv2.imshow("funny", drawn)
            cv2.waitKey(1)
            if cnt <= 0:
                cv2.imwrite("pose.png", drawn)
                self.input.stop()
                break

        pickle.dump(Pose(kps, w, h), open("pose.np", "wb"))

        cv2.destroyAllWindows()
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
