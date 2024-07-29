"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: racecar_vision_with_controller.py

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
global speed
global angle
global speed_offset
global angle_offset
########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed
    global angle
    global speed_offset
    global angle_offset

    speed = 0.0 # The initial speed is at 1.0
    angle = 0.0 # The initial turning angle is 0.0
    speed_offset = 0.45 # The initial speed offset is 0.5
    angle_offset = 0.45 # The inital angle offset is 0.5

    # This tells the car to begin at a standstill
    rc.drive.stop()
   
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
    process_image()

    global speed
    global angle
    global speed_offset
    global angle_offset

    # TODO Part 1: Modify the following conditional statement such that when the
    # right trigger is pressed, the RACECAR moves forward at the designated speed.
    # when the left trigger is pressed, the RACECAR moves backward at the designated speed.
    if rc.controller.get_trigger(rc.controller.Trigger.RIGHT) > 0:
        speed = 1
    elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) > 0:
        speed = -1
    else:
        speed = 0

    # TODO Part 2: Modify the following conditional statement such that when the
    # value of the left joystick's x-axis is greater than 0, the RACECAR's wheels turn right.
    # When the value of the left joystick's x-axis is less than 0, the RACECAR's wheels turn left.
    (x, y) = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    if x > 0:
        angle = 0.5
    elif x < 0:
        angle = -0.5
    else:
        angle = 0

    # TODO Part 3: Write a conditional statement such that when the
    # "A" button is pressed, increase the speed of the RACECAR. When the "B" button is pressed,
    # decrease the speed of the RACECAR. Print the current speed of the RACECAR to the
    # terminal window.
    if rc.controller.is_down(rc.controller.Button.A):
        if (speed + speed_offset > 1):
            speed = 1
        else:
            speed += speed_offset
        print(f"Current Speed: {speed}")
    elif rc.controller.is_down(rc.controller.Button.B):
        if (speed - speed_offset < -1):
            speed = -1
        else:
            speed -= speed_offset
        print(f"Current Speed: {speed}")

    # TODO Part 4: Write a conditional statement such that when the
    # "X" button is pressed, increase the turning angle of the RACECAR. When the "Y" button
    # is pressed, decrease the turning angle of the RACECAR. Print the current turning angle
    # of the RACECAR to the terminal window.
    if rc.controller.is_down(rc.controller.Button.X):
        if (angle + angle_offset > 1):
            angle = 1
        else:
            angle += angle_offset
        print(f"Current Angle: {angle}")
    elif rc.controller.is_down(rc.controller.Button.Y):
        if (angle - angle_offset < -1):
            angle = -1
        else:
            angle -= angle_offset
        print(f"Current Angle: {angle}")

    # Send the speed and angle values to the RACECAR
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
