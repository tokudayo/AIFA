from .base.hpe import HpeModel
import mediapipe as mp

from .LiteHRNet import LiteHRNet

class BlazePose(HpeModel):
    '''Google's BlazePose model is a 3D HPE model that can detect 33 landmarks.'''
    def __init__(self,complexity=1):
        self.model = mp.solutions.pose.Pose(
                    static_image_mode=False,
                    model_complexity=complexity,
                    min_detection_confidence=0.5)

    def forward(self, frame):
        pred = self.model.process(frame)
        if pred.pose_landmarks:
            results = pred.pose_landmarks
        else :
            results = None
        return results

    def draw(self, frame, results):
        '''
        Draw the results on the frame.
        '''
        if results is None:
            return frame
        mp.solutions.drawing_utils.draw_landmarks(frame, results, mp.solutions.pose.POSE_CONNECTIONS)
        return frame

    def predict(self, frame):
        return self.forward(frame)
    
    def __call__(self, frame):
        return self.predict(frame)
    
    def __repr__(self):
        return "BlazePose"

class LiteHRNet(HpeModel):
    
    def __init__(self):
        # LiteHRNet-18 implementation
        base_channel = 16
        cfg=dict(
                stem=dict(stem_channels=32, out_channels=32, expand_ratio=1),
                num_stages=3,
                stages_spec=dict(
                    num_modules=(2, 4, 2),
                    num_branches=(2, 3, 4),
                    num_blocks=(2, 2, 2),
                    module_type=('LITE', 'LITE', 'LITE'),
                    with_fuse=(True, True, True),
                    reduce_ratios=(8, 8, 8),
                    num_channels=(
                        (base_channel, base_channel*2),
                        (base_channel, base_channel*2, base_channel*4),
                        (base_channel, base_channel*2, base_channel*4, base_channel*8),
                    )),
            )
        self.model = LiteHRNet(cfg, in_channels=3)
        #self.model.load_state_dict(torch.load('LiteHRNet.pth'))
        self.model.eval()

    def forward(self, frame):
    
        pred = self.model.process(frame)
        if pred.pose_landmarks:
            #results = self.to_17_landmarks(pred.pose_landmarks)
            results = pred.pose_landmarks
        else :
            results = None
        return results

    def predict(self, frame):
        return self.forward(frame)
    
    def __repr__(self):
        return "LiteHRNet"