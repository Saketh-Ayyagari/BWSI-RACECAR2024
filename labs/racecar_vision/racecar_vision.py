"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: racecar_vision.py

Title: 3.1 Computer Vision Library

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
import racecar_core
import cv2 as cv
import numpy as np

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    rc.drive.set_speed_angle(1, 1)
    rc.drive.set_speed_angle(0, 0)    
def process_image():
    image = rc.camera.get_color_image()

    row, col, pixel_size = image.shape
    # finds the RGB values in the MIDDLE of the screen
    B, G, R = image[row//2][col//2] 

    color = np.zeros((row, col, pixel_size), np.uint8)
    color[:] = (B, G, R)
    cv.namedWindow('BGR Color Display', cv.WINDOW_NORMAL)
    cv.imshow('BGR Color Display', color)
    cv.circle(image, (col//2, row//2), 5, (0, 255, 255), -1) 

    rc.display.show_color_image(image)

    # the order of the center is (col, row) because it simulates x and y coordinates

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    process_image() # Remove 'pass' and write your source code for the update() function here

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
