"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab_3edit.py

Title: Lab 3 - Stoplight Challenge

Author: Saketh Ayyagari 

Purpose: Write a script to enable autonomous behavior from the RACECAR. When
the RACECAR sees a stoplight object (colored cube in the simulator), respond accordingly
by going straight, turning right, turning left, or stopping. Append instructions to the
queue depending on whether the position of the RACECAR relative to the stoplight reaches
a certain threshold, and be able to respond to traffic lights at consecutive intersections. 

THIS IS EDITED TO BE MORE ACCURATE USING CONTROL THEORY PRINCIPLES FROM LAB4

Expected Outcome: When the user runs the script, the RACECAR should control itself using
the following constraints:
- When the RACECAR sees a BLUE traffic light, make a right turn at the intersection
- When the RACECAR sees an ORANGE traffic light, make a left turn at the intersection
- When the RACECAR sees a GREEN traffic light, go straight
- When the RACECAR sees a RED traffic light, stop moving,
- When the RACECAR sees any other traffic light colors, stop moving.

Considerations: Since the user is not controlling the RACECAR, be sure to consider the
following scenarios:
- What should the RACECAR do if it sees two traffic lights, one at the current intersection
and the other at the intersection behind it?
- What should be the constraint for adding the instructions to the queue? Traffic light position,
traffic light area, or both?
- How often should the instruction-adding function calls be? Once, twice, or 60 times a second?

Environment: Test your code using the level "Neo Labs > Lab 3: Stoplight Challenge".
By default, the traffic lights should direct you in a counterclockwise circle around the course.
For testing purposes, you may change the color of the traffic light by first left-clicking to 
select and then right clicking on the light to scroll through available colors.
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
# The smallest contour we will recognize as a valid contour (Adjust threshold!)
MIN_CONTOUR_AREA = 50

# TODO Part 1: Determine the HSV color threshold pairs for ORANGE, GREEN, RED, YELLOW, and PURPLE
# Colors, stored as a pair (hsv_min, hsv_max)
BLUE = ((90, 120, 120), (120, 255, 255))  # The HSV range for the color blue
GREEN = ((40, 50, 50), (70, 255, 255))  # The HSV range for the color green
RED = ((0, 150, 150), (10, 255, 255))  # The HSV range for the color red
ORANGE = ((10, 40, 40), (24, 255, 255)) # The HSV range for the color orange
YELLOW = ((24, 70, 70), (30, 255, 255)) # The HSV range for the color yellow
PURPLE = ((125, 50, 50), (165, 255, 255)) # The HSV range for the color purple

# >> Variables
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour

queue = [] # The queue of instructions
stoplight_color = "" # The current color of the stoplight


########################################################################################
# Functions
########################################################################################

# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area
def update_contour():
    global contour_center
    global contour_area
    global stoplight_color

    image = rc.camera.get_color_image()

    '''
    Few things to note
    OpenCV Coordinates have the x-direction from left to right and the y-direction from top to bottom.
    The coordinates the RACECAR takes are (height, width)
    Resolution of one frame is 480 rows x 640 columns
    '''
    
    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # TODO Part 2: Search for line colors, and update the global variables
        # contour_center and contour_area with the largest contour found
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        colors = [BLUE, GREEN, RED, ORANGE, YELLOW, PURPLE]
        combined_mask = 0
        for c in colors:
            combined_mask += cv.inRange(hsv, c[0], c[1])
        
        contours, _ = cv.findContours(combined_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        filtered_contours = [c for c in contours if cv.contourArea(c) >= MIN_CONTOUR_AREA]

        # finding max contour
        max_contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)
        contour_center = rc_utils.get_contour_center(max_contour)

        if contour_center is not None:

            contour_area = cv.contourArea(max_contour)

            cv.drawContours(image, [max_contour], 0, (255, 255, 0), 3)
            # TODO Part 3: Repeat the search for all potential traffic light colors,
            # then select the correct color of traffic light detected.
            hue = hsv[contour_center[0]][contour_center[1]][0]
            if 0 <= hue < 10 or 165 <= hue <= 180:
                stoplight_color = 'RED'
            elif 10 <= hue < 24:
                stoplight_color = 'ORANGE'
            elif 24 <= hue < 30: 
                stoplight_color = 'YELLOW'
            elif 30 <= hue < 70:
                stoplight_color = 'GREEN'
            elif 90 <= hue < 120:
                stoplight_color = 'BLUE'
            elif 125 <= hue < 165:
                stoplight_color = 'PURPLE'

            cv.circle(image, (contour_center[1], contour_center[0]), 6, (255, 255, 0), -1)
        rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    # Set initial driving speed and angle
    rc.drive.set_speed_angle(0,0)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message (You may edit this to be more informative!)
    print(
        ">> Lab 3 - Stoplight Challenge\n"
        "\n"
        "Controls:\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
        
    global queue, contour_area, contour_center, stoplight_color

    update_contour()
    
    if contour_area < 26000 and len(queue)==0 and stoplight_color not in ["RED", "YELLOW", "PURPLE"]:
        speed = 1
        error = rc.camera.get_width()//2 - contour_center[1]
        angle = rc_utils.remap_range(error, -320, 320, 1, -1)
    # TODO Part 2: Complete the conditional tree with the given constraints.
    else:
        if len(queue) == 0:
            if stoplight_color == "BLUE":
                turnRight()
            elif stoplight_color == "GREEN":
                goStraight()
            elif stoplight_color == "ORANGE":
                turnLeft()         
            else:
                stopNow()
                
            # TODO Part 3: Implement a way to execute instructions from the queue once they have been placed
            # by the traffic light detector logic (Hint: Lab 2)
        
        if len(queue) > 0:
            speed = queue[0][1]
            angle = queue[0][2]
            queue[0][0] -= rc.get_delta_time()
            if queue[0][0] <= 0:
                queue.pop(0)
        else:
            speed = 0
            angle = 0

    # Send speed and angle commands to the RACECAR
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

# [FUNCTION] Appends the correct instructions to make a 90 degree right turn to the queue
def turnRight():
    global queue
    if (len(queue) == 0):
        queue.append([1.35, 1, 1])
    # TODO Part 4: Complete the rest of this function with the instructions to make a right turn

# [FUNCTION] Appends the correct instructions to make a 90 degree left turn to the queue
def turnLeft():
    global queue
    if (len(queue) == 0):
        queue.append([1.208, 1, -1])
    # TODO Part 5: Complete the rest of this function with the instructions to make a left turn

# [FUNCTION] Appends the correct instructions to go straight through the intersectionto the queue
def goStraight():
    global queue
    if (len(queue) == 0):
        queue.append([0.9, 1, 0])
    # TODO Part 6: Complete the rest of this function with the instructions to make a left turn

# [FUNCTION] Clears the queue to stop all actions
def stopNow():
    global queue
    queue.clear()

def update_slow():
    global stoplight_color
    print(stoplight_color)

    


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
