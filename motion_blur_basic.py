# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 14:06:31 2021

@author: Sammy
"""

import cv2
import numpy as np

def process_frame(cur_frame):
    kernel_size = 30
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
    kernel /= kernel_size
    frame = cv2.filter2D(cur_frame, -1, kernel)
    return frame

VIDEO_PATH = "F:\\OBS Files\\"
video_name = "duel_with_ck.mp4"
export_name = "motion_blurred_duel_with_ck.mp4"

vhandle = cv2.VideoCapture(VIDEO_PATH + video_name)
# get size and fps of original video
width = int(vhandle.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vhandle.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vhandle.get(cv2.CAP_PROP_FPS)

# create VideoWriter for saving
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
outVideo = cv2.VideoWriter(export_name, fourcc, fps, (width, height))

# go thru individual frames
success, frame = vhandle.read()
i = 0
while success and i<90:
    frame = process_frame(frame)
    outVideo.write(frame)
    cv2.imshow("mb1", frame)
    cv2.waitKey(2)
    success, frame = vhandle.read()
    i+=1
cv2.destroyAllWindows()
