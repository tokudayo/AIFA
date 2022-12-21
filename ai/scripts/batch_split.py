import os

import cv2


clip_path = './data/clip_sp/c1_3.avi'
out_path = './data/batch_hc3/'

try:
    os.makedirs(out_path)
except FileExistsError:
    pass

cap = cv2.VideoCapture(clip_path)
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

frame_cnt = 0
batch = []

while cap.isOpened():
    frame_cnt += 1
    # print(frame_cnt)
    ret, frame = cap.read()
    if ret == True:
        batch.append(ret)
        if frame_cnt % 10 == 0 and frame_cnt > 0:
        # frame = cv2.flip(frame, 0)
            writer = cv2.VideoWriter(
                os.path.join(out_path, f"{frame_cnt//10}.avi") ,
                fourcc, float(fps),
                (frame_width, frame_height)
            )
            for b in batch:
                writer.write(b)
            writer.release()
        pass
    else:
        break

cap.release()