"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: template.py << [Modify with your own file name!]

Title: Car Follower

Author: Saketh

Purpose: [PLACEHOLDER] << [Write the purpose of the script here]

Expected Outcome: [PLACEHOLDER] << [Write what you expect will happen when you run
the script.]
"""

########################################################################################
# Imports
########################################################################################
import numpy as np
import cv2 as cv
import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
global speed, angle
global marker_center, identification, orientation

marker_center = None
identification = None
orientation = None
COLOR = ((1, 1, 0), (1, 1, 255), 'blue')


########################################################################################
# Functions
########################################################################################
def update_image():
    global marker_center, identification, orientation
    image = rc.camera.get_color_image()
    markers = rc_utils.get_ar_markers(image, [COLOR])
    if len(markers) > 0:
        marker = markers[0]
    # going through markers until it finds desired marker
    
    # getting the marker center 
        if marker is not None:
            top_left, bottom_right = marker.get_corners()[::2]
            column = (top_left[1] + bottom_right[1])//2
            row = (top_left[0] + bottom_right[0])//2
            marker_center = (row, column) # (x, y)
            
            # setting other variables
            identification = marker.get_id()
            orientation = marker.get_orientation()

            rc_utils.draw_ar_markers(image, [marker])
            rc_utils.draw_circle(image, marker_center, (0, 0, 255), 6)
    rc.display.show_color_image(image)
    
# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed, angle
    speed = 0
    angle = 0

    rc.set_update_slow_time(0.5)

    rc.drive.stop()
# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global speed, angle
    global marker_center, identification, orientation
    
    update_image()

    right = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    left = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    if right > 0:
        speed = right
    elif left > 0:
        speed = -left
    else:
        speed = 0
    if marker_center is not None:
        error = rc.camera.get_width()//2 - marker_center[1]
        angle = rc_utils.remap_range(error, -320, 320, 1, -1)

    # Send the speed and angle values to the RACECAR
    rc.drive.set_speed_angle(speed, angle)

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    global speed, angle
    global marker_center, identification, orientation
    print(f"ID: {identification}")
    print(f"Marker center; {marker_center}")
    print(f"Orientation: {orientation}")
    print(f"=======================================")

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
