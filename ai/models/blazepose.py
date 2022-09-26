from typing import List, Literal

import mediapipe as mp
import numpy as np

from ai.base import HpeModel


class BlazePose(HpeModel):
    '''Google's BlazePose is a 3D HPE model that can detect 33 landmarks'''
    def __init__(self,
                 complexity: Literal[0, 1, 2, 3] = 1,
                 static_mode: bool = False,
                 min_detection_confidence: float = 0.5):
        self.model = mp.solutions.pose.Pose(
                    static_image_mode=static_mode,
                    model_complexity=complexity,
                    min_detection_confidence=min_detection_confidence)

    def forward(self, frame: np.array):
        pred = self.model.process(frame)
        if pred.pose_landmarks:
            results = pred.pose_landmarks
        else:
            results = None
        return results

    def draw(self, frame: np.array, results: object):
        '''
        Draw the results on the frame.
        '''
        if results is None:
            return frame
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            results,
            mp.solutions.pose.POSE_CONNECTIONS
        )
        return frame

    def predict(self, frame: np.array):
        return self.forward(frame)

    @staticmethod
    def _blazepose_kp_to_coco_kp(landmarks: List[object]):
        '''
        This function converts the 33 keypoints to 17 keypoints:
                "nose","left_eye","right_eye","left_ear","right_ear",
                "left_shoulder","right_shoulder","left_elbow","right_elbow",
                "left_wrist","right_wrist","left_hip","right_hip",
                "left_knee","right_knee","left_ankle","right_ankle"

        Each formatted as follow, according to COCO format:
                [x, y, z, visibility]
            '''
        # idx of needed keypoints in BlazePose
        idx = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
        # Filter out the keypoints
        landmarks = [landmarks[i] for i in idx]
        # Convert to COCO format
        landmarks = [
            [landmark.x, landmark.y, landmark.z, landmark.visibility]
            for landmark in landmarks
        ]

        return landmarks

    @classmethod
    def postprocess(cls, frame):
        return cls._blazepose_kp_to_coco_kp(frame)

    def __call__(self, frame):
        return self.predict(frame)

    def __repr__(self):
        return "BlazePose"
