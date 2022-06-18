# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 16:31:22 2021

@author: Sammy
"""

import math
import numpy as np

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
    return kernel

while True:
    size = eval(input("size: "))
    angle = eval(input("angle: "))
    print(get_kernel(size, angle))
