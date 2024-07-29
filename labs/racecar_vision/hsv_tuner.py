"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: hsv_tuner.py

Title: [PLACEHOLDER] << [Modify with your own title]

Author: [PLACEHOLDER] << [Write your name or team name here]

Purpose: [PLACEHOLDER] << [Write the purpose of the script here]

Expected Outcome: [PLACEHOLDER] << [Write what you expect will happen when you run
the script.]
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
import racecar_core
import racecar_utils as rc_utils

import pygame
from pygame.locals import *
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
low = ()
high = ()
########################################################################################
# Functions
########################################################################################
def update_contour():
    global low, high
    image = rc.camera.get_color_image()
    if image is not None:
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, low, high)
        rc.display.show_color_iamge(mask)
    
# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    # initializing pygame window
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((1000, 1000))


# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    pass # Remove 'pass' and write your source code for the update() function here

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
