# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 17:30 2021

@author: Sammy
"""

import cv2, math
import numpy as np

X1, X2 = 830, 1070
Y1, Y2 = 464, 610

def process_frame(cur_frame, prev_frame):
    gray = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    gray = gray[Y1:Y2, X1:X2]
    prev_gray = prev_gray[Y1:Y2, X1:X2]
    
    # calculate optical flow by Farneback method
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, gray, None, 0.5, 3, 200, 3, 5, 1.2, 0)
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])    
    frame_motion = np.average(magnitude)
    
    # exception for still frames
    if frame_motion == float("inf"):
        return cur_frame
    
    # change magnitude of motion
    frame_motion = 1 * frame_motion
    frame_motion = int(frame_motion)
    frame_dir = np.average(angle)
    
    # only apply kernel if pixel is moving significantly
    if frame_motion <= 5:
        return cur_frame

    # apply kernel
    kernel = get_kernel(frame_motion, frame_dir)
    frame = cv2.filter2D(cur_frame, -1, kernel)
    return frame

def my_int(x):
    if x-int(x) > 0.5:
        return int(x)+1
    else:
        return int(x)

def get_kernel(size, angle):
    kernel=np.zeros((size,size))
    tan = math.tan(angle)
    if abs(tan) <= 1:
        for x in range(size):
            x_cord = x - (size - 1)/2
            y = x_cord*tan
            y += (size - 1)/2
            y = my_int(y)
            kernel[y][x] = 1
    else:
        cot = 1/tan
        for y in range(size):
            y_cord = y - (size - 1)/2
            x = y_cord*cot
            x += (size - 1)/2
            x = my_int(x)
            kernel[y][x] = 1
    kernel /= size
    return kernel

VIDEO_PATH = "F:\\OBS Files\\"
video_name = "duel_with_ck.mp4"
export_name = "motion_blurred_duel_with_ck.mp4"

vhandle = cv2.VideoCapture(VIDEO_PATH + video_name)
# get size and fps of original video
width = int(vhandle.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vhandle.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vhandle.get(cv2.CAP_PROP_FPS)

# get frame difference
subtractor = cv2.createBackgroundSubtractorMOG2(
    history=5, varThreshold=90, detectShadows=False)

# create VideoWriter for saving
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
outVideo = cv2.VideoWriter(export_name, fourcc, fps, (width, height))

# go thru individual frames
success, frame = vhandle.read()
prev_frame = frame
i = 0
while success:
    frame = process_frame(frame, prev_frame)
    outVideo.write(frame)
    cv2.imshow("motion blur", frame)
    cv2.waitKey(2)
    prev_frame = frame
    success, frame = vhandle.read()
    i+=1
cv2.destroyAllWindows()
