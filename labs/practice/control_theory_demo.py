"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: control_theory_demo.py
Title: Control Theory Demos
Author: Saketh Ayyagrari
Purpose: [PLACEHOLDER] << [Write the purpose of the script here]

Expected Outcome: [PLACEHOLDER] << [Write what you expect will happen when you run
the script.]
"""

########################################################################################
# Imports
########################################################################################

import sys
import numpy as np
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

global line_center
global angle, speed
speed = 0.9

MIN_CONTOUR = 50


########################################################################################
# Functions
########################################################################################

'''
rc_utils.get_contour_center(c) returns a (row, col) tuple
'''

def update_line():
    image = rc.camera.get_color_image()
    image = rc_utils.crop(image, (360, 0), (rc.camera.get_height(), rc.camera.get_width()))
    # creating mask of image 
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    low = (80, 50, 50); high = (125, 255, 255)
    mask = cv.inRange(hsv, low, high)
    # drawing max contour (line) and getting the center

    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        max_contour = contours[0]
        for c in contours:
            if cv.contourArea(c) > cv.contourArea(max_contour):
                max_contour = c
        cv.drawContours(image, [max_contour], -1, (0, 255, 0), 2)

        global line_center
        line_center = rc_utils.get_contour_center(max_contour)

        cv.circle(image, (line_center[1], line_center[0]), 4, (255, 255, 0), -1)
        cv.circle(image, (340, line_center[0]), 4, (0, 0, 255), -1)
        rc.display.show_color_image(image)
'''
def bang_bang_control(line: int, setpoint: int): # given the x-values of the line and the setpoint
    global angle
    error = setpoint - line
    if error > 0: # line is to the left
        angle = -1
    elif error < 0: # line is to the right
        angle = 1
    else: # line is in the center
        angle = 0
    return angle
'''
def proportional_control(line: int, setpoint: int):
    error = setpoint - line
    angle = rc_utils.remap_range(error, 320, -rc.camera.get_width()/2, -1, 1)
    '''
    angle = rc_utils.remap_range(line_position, 0, rc.camera.get_width(), -1, 1)
    '''
    return angle

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    rc.drive.set_speed_angle(0, 0)

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global angle, speed
    update_line()
    angle = proportional_control(setpoint=640/2, line=line_center[1])
    rc.drive.set_speed_angle(speed, angle)
    

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    pass # Remove 'pass and write your source code for the update_slow() function here


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
