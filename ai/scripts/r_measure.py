from threading import Thread

import cv2
from aifa.base.pose import Pose

from aifa.utils import Timer
from aifa.inputs import Cv2VideoStream
from aifa.models import BlazePose
from aifa.experimental.r_sp import ShoulderPress

r = 0.01
sample = 1

ref = ["""static
static
static
up
up
up
top
static
static
static
down
down
down
down
bottom
""", """static
static
static
static
static
up
up
up
up
top
static
static
down
down
down
""", """down
bottom
static
static
static
up
up
up
top
static
down
down
down
down
"""]
states = ref[sample - 1].split('\n')
print(states)

class AIFlow(object):
    def __init__(self):
        self.input = Cv2VideoStream(f"./data/clip_sp/c1_{sample}.avi", max_size=720, max_queue_size=1)
        self.model = BlazePose(complexity=1, static_mode=False)
        self.evaluator = ShoulderPress(r=r)

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        self.input.start()
        cnt = 0
        correct = 0
        while not self.input.stopped:
            frame = self.input.get_frame()
            if frame is None:
                continue
            frame = cv2.flip(frame, 0)
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
            if results:
                print(results)
                if results == states[cnt//10 - 1]:
                    correct += 1
                else:
                    print("Incorrect")
            
            # cv2.imshow("funny", drawn)
            # if cv2.waitKey(1) == ord('q'):
            #     self.input.stop()
            #     break

        cv2.destroyAllWindows()
        print(f"{correct}/{cnt//10} correct")
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
