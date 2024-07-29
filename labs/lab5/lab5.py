"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab5.py

Title: Lab 5 - Cone Parking

Author: Saketh Ayyagari 

Purpose: This script provides the RACECAR with the ability to autonomously detect an orange
cone and then drive and park 30cm away from the cone. Complete the lines of code under the 
#TODO indicators to complete the lab.

Expected Outcome: When the user runs the script, the RACECAR should be fully autonomous
and drive without the assistance of the user. The RACECAR drives according to the following
rules:
- The RACECAR detects the orange cone using its color camera, and can navigate to the cone
and park using its color camera and LIDAR sensors.
- The RACECAR should operate on a state machine with multiple states. There should not be
a terminal state. If there is no cone in the environment, the program should not crash.

Environment: Test your code using the level "Neo Labs > Lab 5: Cone Parking".
Click on the screen to move the orange cone around the screen.
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np
from enum import IntEnum

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30

# TODO Part 1: Determine the HSV color threshold pairs for ORANGE
ORANGE = ((10, 50, 10), (20, 255, 255)) # The HSV range for the color orange

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0
state = None
DISTANCE = 50

########################################################################################
# state Machine 
########################################################################################
class State(IntEnum):
    WANDER = 0
    APPROACH = 1
    STOP = 2

########################################################################################
# Functions
########################################################################################

# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area
def update_contour():
    global contour_center, contour_area
    global state

    image = rc.camera.get_color_image()

    contours_cone = rc_utils.find_contours(image, ORANGE[0], ORANGE[1])
    cone_contour = rc_utils.get_largest_contour(contours_cone, MIN_CONTOUR_AREA)
    contour_center = rc_utils.get_contour_center(cone_contour)
    if contour_center is not None:
        contour_area = cv.contourArea(cone_contour)
    

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed
    global angle
    global state

    # Initialize variables
    speed = 0
    angle = 0

    rc.drive.stop()

    state = State.WANDER

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message
    print(
        ">> Lab 4 - Line Follower\n"
        "\n"
        "Controls:\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  

def update():
    global speed
    global angle
    global state
    global contour_center
    global DISTANCE

    # Search for contours in the current color image
    update_contour()
    
    # TODO Part 3: Park the car 30cm away from the closest orange cone.
    # You may use a state machine and a combination of sensors (color camera,
    # or LIDAR to do so). Depth camera is not allowed at this time to match the
    # physical RACECAR Neo.
    
    if state == State.WANDER: # wander state -> car will move in a circle
        speed = 1
        angle = 1
        if contour_center is not None:
            state = State.APPROACH
    elif state == State.APPROACH:
        if contour_center is None:
            state = State.WANDER
        else:
            SETPOINT = rc.camera.get_width()//2
            error = SETPOINT - contour_center[1]
            angle = rc_utils.remap_range(error, -320, 320, 1, -1)
            # getting lidar scans
            
            scans = rc.lidar.get_samples()
            forward = rc_utils.get_lidar_closest_point(scans)
            print(f"Closest point(s): {forward}")
            speed = rc_utils.clamp(rc_utils.remap_range(forward[1], DISTANCE, 1000, 0, 1), 0, 1)
            if forward[1] < DISTANCE:
                state = State.STOP
    elif state == State.STOP:
        speed = 0
        angle = 0
    
    # Set the speed and angle of the RACECAR after calculations have been complete
    rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x-position
    if rc.camera.get_color_image() is None:
        # If no image is found, print all X's and don't display an image
        print("X" * 10 + " (No image) " + "X" * 10)
    else:
        # If an image is found but no contour is found, print all dashes
        if contour_center is None:
            print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
        else:
            s = ["-"] * 32
            s[int(contour_center[1] / 20)] = "|"
            print("".join(s) + " : area = " + str(contour_area))

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()