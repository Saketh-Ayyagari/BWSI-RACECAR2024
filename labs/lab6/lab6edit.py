"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab6.py

Title: Lab 6 - Wall Follower

Author: [PLACEHOLDER] << [Write your name or team name here]

Purpose: This script provides the RACECAR with the ability to autonomously follow a wall.
The script should handle wall following for the right wall, the left wall, both walls, and
be flexible enough to handle very narrow and very wide walls as well.

Expected Outcome: When the user runs the script, the RACECAR should be fully autonomous
and drive without the assistance of the user. The RACECAR drives according to the following
rules:
- The RACECAR detects a wall using the LIDAR sensor a certain distance and angle away.
- Ideally, the RACECAR should be a set distance away from a wall, or if two walls are detected,
should be in the center of the walls.
- The RACECAR may have different states depending on if it sees only a right wall, only a 
left wall, or both walls.
- Both speed and angle parameters are variable and recalcualted every frame. The speed and angle
values are sent once at the end of the update() function.

Note: This file consists of bare-bones skeleton code, which is the bare minimum to run a 
Python file in the RACECAR sim. Less help will be provided from here on out, since you've made
it this far. Good luck, and remember to contact an instructor if you have any questions!

Environment: Test your code using the level "Neo Labs > Lab 6: Wall Follower".
Use the "TAB" key to advance from checkpoint to checkpoint to practice each section before
running through the race in "race mode" to do the full course. Lowest time wins!
"""

########################################################################################
# Imports
########################################################################################

import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import numpy as np
import cv2 as cv
import math
import racecar_core
import racecar_utils as rc_utils
from enum import IntEnum
from WallFollower import WallFollower

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()
wall_follower = WallFollower(rc)

# Declare any global variables here
global speed, angle, state
global scans
speed = 0
angle = 0
state = None
Kp = 0; Ki = 0; Kd = 0 
int_sum = 0

prevError = None

class State(IntEnum):
    L = 0 # Only left wall is visible
    R = 1 # Only right wall is visible
    LandR = 2 # Both walls are visible

PI = math.pi; SIN = math.sin; COS = math.cos; ARCSIN = math.asin; ATAN2 = math.atan2 
SQRT = math.sqrt; ABS = abs; RAD = math.radians; DEG = math.degrees

########################################################################################
# Functions
########################################################################################
def camera():
    image = rc.camera.get_color_image()
    ar_markers = rc_utils.get_ar_markers(image)

    rc_utils.draw_ar_markers(image, ar_markers)

    rc.display.show_color_image(image)


# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed, angle
    global Kp, Ki, Kd
    speed = 0
    angle = 0
    
    # NOTE: PID Values for default speed (~1 m/s)
    # Kp = 0.071
    # Ki = 0
    # Kd = 0.00083

    Kp = 0.035
    Ki = 0#.003125
    Kd = 0#.001
    rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global speed, angle
    global left, right
    global Kp, Ki, Kd
    global state
    
    global scans, error
    global P_error, D_error
    global int_sum
    global prevError
    
    speed, angle = wall_follower.update()
        
    rc.drive.set_speed_angle(speed, angle)

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    global speed, angle
    global left, right
    global Kp, Ki, Kd
    global state
    global error_log
    global scans, error
    global P_error, D_error
    print(f"Angle between left wall relative to RACECAR: {wall_follower.print_left_error()}")
    print(f"Angle between right wall relative to RACECAR: {wall_follower.print_right_error()}")
    print(f"(Speed, Angle): ({wall_follower.get_speed()}, {wall_follower.get_angle()})")
    print("="*75)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()


