"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab4.py

Title: Lab 4 - Line Follower

Author: Saketh Ayyagari 

Purpose: Write a script to enable fully autonomous behavior from the RACECAR. The
RACECAR should automatically identify the color of a line it sees, then drive on the
center of the line throughout the obstacle course. The RACECAR should also identify
color changes, following colors with higher priority than others. Complete the lines 
of code under the #TODO indicators to complete the lab.

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
MIN_CONTOUR_AREA = 45

# A crop window for the floor directly in front of the car
CROP_FLOOR = ((340, 0), (rc.camera.get_height()-25, rc.camera.get_width())) # crop floor for line detection
CONE_CROP = ((150, 0), (400, rc.camera.get_width())) # crop image for cone detection

# TODO Part 1: Determine the HSV color threshold pairs for BLUE, GREEN, and RED

BLUE = ((80, 65, 70), (120, 255, 255))  # The HSV range for the color blue
GREEN = ((40, 50, 50), (80, 255, 255))  # The HSV range for the color green
RED = ((0, 200, 200), (10, 255, 255))  # The HSV range for the color red

WHITE = ((0, 60, 150), (179, 70, 255)) # The HSV range for the color white
YELLOW = ((20, 0, 25), (40, 255, 255)) # The HSV range for the color yellow
PURPLE = ((125, 50, 25), (165, 255, 255)) # The HSV range for the color purple
BLACK = ((0, 50, 0), (179, 255, 56)) # The HSV range for the color black
ORANGE = ((10, 50, 10), (20, 255, 255)) # The HSV range for the color orange
PINK = ((90, 150, 150), (179, 230, 255)) # The HSV range for the color pink

# Color priority: Red >> Green >> Blue
COLOR_PRIORITY = None
# All possible color priorities
COLOR_PRIORITY_WHITE = (RED, GREEN, BLUE)
COLOR_PRIORITY_PURPLE = (BLUE, RED, GREEN)
COLOR_PRIORITY_YELLOW = (RED, BLUE, GREEN)
COLOR_PRIORITY_ORANGE = (BLUE, GREEN, RED)
COLOR_PRIORITY_BLACK = (GREEN, RED, BLUE)
COLOR_PRIORITY_PINK = (GREEN, BLUE, RED)

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
COLOR = None
cone_area = 0
########################################################################################
# Functions
########################################################################################

# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area

def update_contour():
    global contour_center, contour_area
    global COLOR_PRIORITY, COLOR
    global cone_area
    image = rc.camera.get_color_image()

    # TODO Part 2: Complete this function by cropping the image to the bottom of the screen,
    # analyzing for contours of interest, and returning the center of the contour and the
    # area of the contour for the color of line we should follow (Hint: Lab 3)

    line_img = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])
    cone_img = rc_utils.crop(image, CONE_CROP[0], CONE_CROP[1])

    contours = None
    for c in COLOR_PRIORITY:
        contour_list = rc_utils.find_contours(line_img, c[0], c[1])
        center = rc_utils.get_contour_center(rc_utils.get_largest_contour(contour_list, MIN_CONTOUR_AREA))
        if center is not None:
            contours = contour_list
            break    
    if contours is not None:
        desired_contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)       
        contour_center = rc_utils.get_contour_center(desired_contour)
        contour_area = cv.contourArea(desired_contour)
        cv.circle(line_img, (contour_center[1], contour_center[0]), 4, (0, 255, 0), -1)
        cv.drawContours(line_img, [c for c in contours if cv.contourArea(c) > MIN_CONTOUR_AREA]
                        , -1, (0, 255, 0), 2)
    
    # looks for cone contours
    cone_contours = rc_utils.find_contours(cone_img, COLOR[0], COLOR[1])
    cone_contour = rc_utils.get_largest_contour(cone_contours, MIN_CONTOUR_AREA)       
    if cone_contour is not None:
        contour_area = cv.contourArea(cone_contour)
        cv.drawContours(cone_img, [c for c in cone_contours if cv.contourArea(c) > MIN_CONTOUR_AREA], 
                        -1, (0, 255, 0), 2)
        
    
    image[CONE_CROP[0][0]:CONE_CROP[1][0]][CONE_CROP[0][1]:CONE_CROP[1][1]] = cone_img
    image[CROP_FLOOR[0][0]:CROP_FLOOR[1][0], CROP_FLOOR[0][1]:CROP_FLOOR[1][1]] = line_img
    rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed, angle
    global COLOR_PRIORITY, COLOR
    
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
    global COLOR, COLOR_PRIORITY

    if rc.controller.was_pressed(rc.controller.Button.A):
        COLOR_PRIORITY = COLOR_PRIORITY_WHITE
        COLOR = WHITE
    elif rc.controller.was_pressed(rc.controller.Button.B):
        COLOR_PRIORITY = COLOR_PRIORITY_PINK
        COLOR = PINK
    elif rc.controller.was_pressed(rc.controller.Button.X):
        COLOR_PRIORITY = COLOR_PRIORITY_BLACK
        COLOR = BLACK
    elif rc.controller.was_pressed(rc.controller.Button.Y):
        COLOR_PRIORITY = COLOR_PRIORITY_PURPLE
        COLOR = PURPLE
    elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) == 1:
        COLOR_PRIORITY = COLOR_PRIORITY_ORANGE
        COLOR = ORANGE
    elif rc.controller.get_trigger(rc.controller.Trigger.RIGHT) == 1:
        COLOR_PRIORITY = COLOR_PRIORITY_YELLOW
        COLOR = YELLOW

    # Search for contours in the current color image
    if COLOR is not None:
        update_contour()

    # TODO Part 3: Determine the angle that the RACECAR should receive based on the current 
    # position of the center of line contour on the screen. Hint: The RACECAR should drive in
    # a direction that moves the line back to the center of the screen.
    
    # Choose an angle based on contour_center
    # If we could not find a contour, keep the previous angle
    
    if contour_center is not None:
        error = (rc.camera.get_width() // 2) - contour_center[1]
        angle = rc_utils.remap_range(error, 320, -320, -1, 1)

    # TODO Part 4: Determine the speed that the RACECAR should drive at. This may be static or
    # variable depending on the programmer's intent.
        if contour_area < 4750:
            speed = 1 - abs(rc_utils.remap_range(error, -320, 320, -0.75, 0.75))
        else:
            speed = 0
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