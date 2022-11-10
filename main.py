from threading import Thread

import cv2
from ai.base.pose import Pose

from utils import Timer
from ai.inputs import Cv2VideoStream, Cv2WebcamStream
from ai.models import BlazePose
from ai.exercises import ShoulderPress
from ai.experimental.exp_shoulder_press import ShoulderPress as exp_ShoulderPress
from kafka import KafkaConsumer, KafkaProducer
from ai.exercises.utils import postprocess_packet

class AIFlow(object):
    def __init__(self):
        # Experimental
        # self.evaluator = exp_ShoulderPress()
        self.evaluator = ShoulderPress()
        self.kafkaConsumer = KafkaConsumer(
            'process.payload', bootstrap_servers='localhost:29091', group_id='my-group')
        self.kafkaProducer = KafkaProducer(bootstrap_servers='localhost:29091')
        self.exercise = None

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):

        for msg in self.kafkaConsumer:
            # print('Retreive')
            # print(msg.value)
            kps = postprocess_packet(msg.value.decode("utf-8"))
            results = (self.evaluator.update(Pose(kps)))
            
            print(results)

            # if eval: print(eval)
            # # flip horizontally
            # drawn = cv2.flip(drawn, 1)
            # cv2.imshow("funny", drawn)
            # if cv2.waitKey(1) == ord('q'):
            #     break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    flow = AIFlow()
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
