from threading import Thread

import cv2
from aifa.base.pose import Pose

from aifa.utils import Timer
from aifa.inputs import Cv2VideoStream, Cv2WebcamStream
from aifa.models import BlazePose
from aifa.exercises import ShoulderPress, HammerCurl, DeadLift

def draw_line_cv2(img, p1, p2, color=(0, 255, 0), thickness=2):
    cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), color, thickness)


class AIFlow(object):
    def __init__(self):
        #self.input = Cv2VideoStream("videos/deadlift/deadlift 2.mp4", max_size=720)
        self.input = Cv2WebcamStream()
        # self.model = DummyHpeModel()
        self.model = BlazePose(complexity=1, static_mode=False)
        # Experimental
        #self.evaluator = exp_ShoulderPress()
        self.evaluator = DeadLift()

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
            h, w, _ = frame.shape
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


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    flow = AIFlow()
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
