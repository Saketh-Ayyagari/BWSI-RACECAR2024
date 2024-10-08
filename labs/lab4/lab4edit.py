"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab4edit.py

Title: Lab 4 - Line Follower

Author: Saketh Ayyagari 

Purpose: Write a script to enable fully autonomous behavior from the RACECAR. The
RACECAR should automatically identify the color of a line it sees, then drive on the
center of the line throughout the obstacle course. The RACECAR should also identify
color changes, following colors with higher priority than others. Complete the lines 
of code under the #TODO indicators to complete the lab.

THIS LAB IS EDITED FOR MORE EXPERIMENTAL PURPOSES

Expected Outcome: When the user runs the script, the RACECAR should be fully autonomous
and drive without the assistance of the user. The RACECAR drives according to the following
rules:
- The RACECAR maintains a following behavior by keeping the line in the center of the screen
- The RACECAR's color priority is RED > GREEN > BLUE.
- The angle of the RACECAR is variable, and is calculated after every frame
- The speed of the RACECAR may be static or variable, depending on the programmer's intents
- The RACECAR must adjust to challenges such as ramps, sharp turns, and dead ends

Environment: Test your code using the level "Neo Labs > Lab 4: Line Follower".
Use the "TAB" key to advance from checkpoint to checkpoint to practice each section before
running through the race in "race mode" to do the full course. Lowest time wins!
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

from LineFollower import LineFollower

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

# A crop window for the floor directly in front of the car
CROP_FLOOR = ((360, 0), (rc.camera.get_height()-15, rc.camera.get_width())) # crop floor for line detection
CONE_CROP = ((150, 0), (330, rc.camera.get_width())) # crop image for cone detection

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour


line_follower = LineFollower(rc)


########################################################################################
# Functions
########################################################################################



# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed, angle
    
    # Initialize variables
    speed = 0
    angle = 0

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
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle
    global contour_area, contour_center
    global Kd, Kp, Ki
    global integral_sum
    
    global errors
    


    # line_follower.update() chooses an angle based on contour_center
    # If we could not find a contour, keep the previous angle
    speed, angle = line_follower.update()
    contour_center = line_follower.get_center()
    contour_area = line_follower.get_area()
     

    # TODO Part 4: Determine the speed that the RACECAR should drive at. This may be static or
    # variable depending on the programmer's intent.
    
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
    global contour_center, contour_area
    global angle
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
    print(f"Proportional Error: {line_follower.get_P_error()}")
    print(F"Integral Error: {line_follower.get_I_error()}")
    print(f"Derivative Error: {line_follower.get_D_error()}")
    print(f"Corrected angle: {angle}")

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()