import math


def deg_to_rad(deg):
    return deg * math.pi / 180


def rad_to_deg(rad):
    return rad * 180 / math.pi


def postprocess_packet(landmarks: ):
    '''
    Convert the packet to a list of landmarks
    '''
    # idx of needed keypoints in BlazePose
    idx = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
    # Filter out the keypoints
    landmarks = [landmarks[i] for i in idx]
    # Convert to COCO format
    landmarks = [
        [float(landmark['x']), float(landmark['y']), float(landmark['z']), float(landmark['visibility'])]
        for landmark in landmarks
    ]

    return landmarks
