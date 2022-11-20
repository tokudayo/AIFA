import os

from threading import Thread

from ai.base.pose import Pose
import json

from ai.utils import Timer
from ai.exercises import ShoulderPress
from kafka import KafkaConsumer, KafkaProducer
from ai.exercises.utils import postprocess_packet

class AIFlow(object):
    def __init__(self):
        # Experimental
        # self.evaluator = exp_ShoulderPress()
        self.evaluator = ShoulderPress()
        self.kafka_consumer = KafkaConsumer(
            'process.payload', bootstrap_servers=os.environ['KAFKA_URL'], group_id='my-group')
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.environ['KAFKA_URL'])
        self.exercise = None

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):

        for msg in self.kafka_consumer:
            # print(msg.value)
            req = json.loads(msg.value.decode("utf-8"))
            kps = postprocess_packet(req)
            results = (self.evaluator.update(Pose(kps)))

            if results is not None:
                self.kafka_producer.send('process.payload.reply', str.encode(
                    json.dumps([req["room"], results], separators=(',', ':'))))


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    flow = AIFlow()
    thread = flow.start()
    thread.join()
    timer.stop()

    print(f"Elapsed: {timer.elapsed:.2f}s")
