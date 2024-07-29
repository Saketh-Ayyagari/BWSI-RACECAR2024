"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab1.py

Title: Lab 1 - RACECAR Controller with best attempt for line following

Author: Team 8: Saketh, Chris, Sophie, Cian

Purpose: Using a Python script and the data polled from the controller module,
write code to replicate a manual control scheme for the RACECAR. Gain a mastery
in using conditional statements, controller functions and an understanding in the
rc.drive.set_speed_angle() function. Complete the lines of code under the #TODO indicators 
to complete the lab.

Expected Outcome: When the user runs the script, they are able to control the RACECAR
using the following keys:
- When the right trigger is pressed, the RACECAR drives forward
- When the left trigger is pressed, the RACECAR drives backward
- When the left joystick's x-axis has a value of greater than 0, the RACECAR's wheels turns to the right
- When the left joystick's x-axis has a value of less than 0, the RACECAR's wheels turns to the left
- When the "A" button is pressed, increase the speed and print the current speed to the terminal window
- When the "B" button is pressed, reduce the speed and print the current speed to the terminal window
- When the "X" button is pressed, increase the turning angle and print the current turning angle to the terminal window
- When the "Y" button is pressed, reduce the turning angle and print the current turning angle to the terminal window

Environment: Test your code using the level "Neo Labs > Lab 1: RACECAR Controller".
"""

########################################################################################
# Imports
########################################################################################

import sys
import numpy as np
import cv2 as cv
from enum import IntEnum
from LaneFollowerController import LaneFollower

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()
lane_follower = LaneFollower(rc)

# Declare any global variables here
MIN_CONTOUR_AREA = 40
BLUE = ((90, 120, 120), (120, 255, 255))  # The HSV range for the color blue
GREEN = ((40, 50, 50), (70, 255, 255))  # The HSV range for the color green
RED = ((0, 150, 150), (10, 255, 255))  # The HSV range for the color red
ORANGE = ((10, 70, 55), (24, 255, 255)) # The HSV range for the color orange
YELLOW = ((24, 70, 70), (30, 255, 255)) # The HSV range for the color yellow
PURPLE = ((125, 50, 50), (165, 255, 255)) # The HSV range for the color purple

soeed, angle = 0, 0
contour_center1 = None
contour_center2 = None
state = None

########################################################################################
# Functions
########################################################################################


# [FUNCTION] The start function is run once every time the start button is pressed



def start():
   global speed
   global angle

   speed = 0.0 # The initial speed is at 1.0
   angle = 0.0 # The initial turning angle is 0.0

   # Set update_slow to refresh every half second
   rc.set_update_slow_time(0.125)

   # This tells the car to begin at a standstill
   rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
   global speed, angle
   global contour_center1, contour_center2
   global state
   
   lane_follower.update_contours()
   angle = lane_follower.update()[1]
   
   speed = 1
   '''
   angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
   '''
   state = lane_follower.get_state()
   rc.drive.set_speed_angle(speed, angle) 


   # Send the speed and angle values to the RACECAR
   rc.drive.set_speed_angle(speed, angle)
def update_slow():
   global speed, angle
   global contour_center1, contour_center2
   global state
   print(f"State: {state}")
   

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
