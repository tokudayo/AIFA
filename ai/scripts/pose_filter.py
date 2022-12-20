import math
import pickle
from threading import Thread

import cv2
from aifa.base.pose import Pose
from aifa.exercises.utils import rad_to_deg
from aifa.utils import Timer
from aifa.inputs import Cv2WebcamStream
from aifa.models import BlazePose

default_angles = [['lr_shoulder', 'l_side'], ['lr_shoulder', 'r_side'], ['l_side', 'lr_hip'], ['r_side', 'lr_hip']]
default_ratios = [
    ['lr_shoulder', 'lr_hip'],
    ['l_side', 'r_side'],
    ['l_side', 'lr_hip'],
]
default_template = {
    'angles': default_angles,
    'ratio': default_ratios,
}

# define comp func
def comp(p1, p2, template, max_angle_diff=30, max_ratio_diff=1):
    # compare angles
    for angle in template['angles']:
        a1 = p1.angle(*angle)
        a2 = p2.angle(*angle)
        # print(a1, a2)
        agl = rad_to_deg(min(abs(a1 - a2), math.pi - abs(a1 - a2)))
        if agl > max_angle_diff:
            print("wrong angle")
            return False
    for kp_a, kp_b in template['ratio']:
        r11 = p1.kp_vector(kp_a)
        r12 = p1.kp_vector(kp_b)
        r21 = p2.kp_vector(kp_a)
        r22 = p2.kp_vector(kp_b)
        # print(r11.magnitude, r12.magnitude, r21.magnitude, r22.magnitude)
        ratio1 = r11.magnitude / r12.magnitude
        ratio2 = r21.magnitude / r22.magnitude
        if abs(ratio1 - ratio2) > max_ratio_diff:
            print("wrong ratio")
            return False
    print("ok")
    return True
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
        correct_pose = pickle.load(open("pose.np", "rb"))
        print("load ok")
        while not self.input.stopped:
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
            pose = Pose(kps, w, h)
            # print(pose, correct_pose)
            comp(pose, correct_pose, default_template)
            cv2.imshow("funny", drawn)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.input.stop()
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    timer = Timer()
    timer.start()
    flow = AIFlow()
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
