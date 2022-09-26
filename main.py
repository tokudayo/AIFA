from threading import Thread
import cv2

from ai.base.utils import Timer, blazepose_kp_to_coco_kp
from ai.input import Cv2VideoStream, WebcamStream
from ai.dummy import DummyHpeModel
from ai.models import BlazePose
from ai.exercises import ShoulderPress


class AIFlow(object):
    def __init__(self):
        # self.input = Cv2VideoStream("sample.mp4")
        self.input = WebcamStream()
        # self.model = DummyHpeModel()
        self.model = BlazePose()
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
            if frame is None: continue
            keypoints = self.model(frame)
            drawn = self.model.draw(frame, keypoints)
            
            if keypoints is None: continue

            results = blazepose_kp_to_coco_kp(keypoints.landmark)

            self.evaluator.update(results)
            state = self.evaluator.state
            if state != 'none':
                print(self.evaluator.state)

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