import os

import cv2
import yaml
from yaml.loader import SafeLoader


meta_path = './meta/sp1.yaml'
out_path = './clip_hc/'

try:
    os.mkdir(out_path)
except FileExistsError:
    pass

with open(meta_path, 'r') as f:
    meta = yaml.load(f, Loader=SafeLoader)
    print(meta)

for file in meta:
    fp = file['fp']
    fn = file['fp'].split('/')[-1].split('.')[0]
    segs = file['split']
    print(f"Processing {fp} with {len(segs)} segments")
    # parts = [(x[0], x[1]) for x in segs]
    # labels = [x[2] for x in segs]

    cap = cv2.VideoCapture(fp)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    writers = [
        cv2.VideoWriter(
            os.path.join(out_path, f"{fn}_{cnt + 1}.avi") ,
            fourcc, float(fps),
            (frame_width, frame_height)
        ) for cnt in range(len(segs))
    ]

    segs = [(int(start * fps), int(end * fps), label) for start, end, label in segs]
    max_frame = int(max([x[1] for x in segs]))

    f = 0
    while cap.isOpened():
        f += 1
        if f > max_frame:
            break
        ret, frame = cap.read()
        if ret == True:
            # frame = cv2.flip(frame, 0)
            for i, seg in enumerate(segs):
                start, end, label = seg
                if start <= f <= end:
                    writers[i].write(frame)
        else:
            break

    for writer in writers:
        writer.release()

    cap.release()