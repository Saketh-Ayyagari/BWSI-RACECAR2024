"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: template.py << [Modify with your own file name!]
"""

########################################################################################
# Imports
########################################################################################

import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
speed = 0; angle = 0

########################################################################################
# Functions
########################################################################################


matrix_default = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0, 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
                            ])
'''
Dot matrix methods
'''
def straight_arrow():
    m = np.copy(matrix_default)
    m[3:-2, 0:22] = 1
    m[4:6, 22] = 1
    m[:, -8:-6] = 1
    m[-6, 1] = 1; m[-6, -2] = 1
    return m
def right_angle_left():
    m = np.copy(matrix_default)
    m[4:, :-4] = 1
    m[:, -8:-5] = 1
    m[0:3, -8] = 1; m[0:3, -4]
    m[1:3, -9] = 1; m[1:3, -3] = 1;
    m[-2, 2] = 1; m[-10, 2] = 1
    return m
def right_angle_right():
    m = right_angle_left()
    m = np.flipud(m)
    return m
        


# [FUNCTION] The start function is run once every time the start button is pressed
def start():
   speed = 0
   angle = 0
   rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    scans = rc.lidar.get_samples()
    print(f"Distance in front of car: {rc_utils.get_lidar_average_distance(scans, 0)}")
    print(f"Distance to right of car: {rc_utils.get_lidar_average_distance(scans, 90)}")
    print(f"Distance to left of car: {rc_utils.get_lidar_average_distance(scans, 270)}")
    print(f"=========================================")

    

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    pass 


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
