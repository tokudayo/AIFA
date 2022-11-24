import json
import os
from threading import Thread

from kafka import KafkaConsumer, KafkaProducer

from aifa.base.pose import Pose
from aifa.utils import Timer
from aifa.exercises import ShoulderPress, DeadLift, HammerCurl


def extract_info(data):
    '''
    Convert the packet to a list of landmarks
    '''
    # idx of needed keypoints in BlazePose
    idx = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
    # Filter out the keypoints
    landmarks = data["data"]
    landmarks = [landmarks[i] for i in idx]
    # Convert to COCO format
    landmarks = [
        [float(landmark['x']), float(landmark['y']), float(landmark['z']), float(landmark['visibility'])]
        for landmark in landmarks
    ]

    return data['exercise'], data['width'], data['height'], landmarks


class AIFlow(object):
    def __init__(self):
        self.recent_ex = None
        self.kafka_consumer = KafkaConsumer(
            'process.payload', bootstrap_servers=os.environ['KAFKA_URL'], group_id='my-group')
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.environ['KAFKA_URL'])

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        for msg in self.kafka_consumer:
            data = json.loads(msg.value.decode("utf-8"))
            ex, width, height, kps = extract_info(data)

            if ex != self.recent_ex:
                self.recent_ex = ex
                if ex == 'shoulder_press':
                    self.evaluator = ShoulderPress()
                elif ex == 'deadlift':
                    self.evaluator = DeadLift()
                elif ex == 'hammer_curl':
                    self.evaluator = HammerCurl()
                else:
                    raise ValueError(f'Unknown exercise {ex}')

            results = self.evaluator.update(Pose(kps, width, height))

            if results is not None:
                self.kafka_producer.send('process.payload.reply', str.encode(
                    json.dumps([data["room"], results], separators=(',', ':'))))


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    flow = AIFlow()
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
