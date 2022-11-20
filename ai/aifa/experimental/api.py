from ast import Str
from typing import List, Union
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import numpy as np
from aifa.exercises import ShoulderPress
from aifa.base.pose import Pose

class Landmark(BaseModel):
    x: float
    y: float
    z: float
    visibility: float

class InputPacket(List[Landmark]):
    pass

def postprocess_packet(landmarks: List[object]):
        '''
        Convert the packet to a list of landmarks
        '''
        # idx of needed keypoints in BlazePose
        idx = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
        # Filter out the keypoints
        landmarks = [landmarks[i] for i in idx]
        # Convert to COCO format
        landmarks = [
            [landmark['x'], landmark['y'], landmark['z'], landmark['visibility']]
            for landmark in landmarks
        ]

        return landmarks

# Define a router to handle each endpoint
class APIFlow:
    def __init__(self):
        self.evaluator = ShoulderPress()
        self.router = APIRouter()
        self.router.add_api_route("/shoulderpress", self.shoulderpress, methods=["POST"])
    
    # Route for keypoints from web front
    def shoulderpress(self, packet: InputPacket):
        landmark = postprocess_packet(packet)
        result = self.evaluator.update(Pose(np.array((landmark))))
        return result


app = FastAPI()
flow = APIFlow()
app.include_router(flow.router)

