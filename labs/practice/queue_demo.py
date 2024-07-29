"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: queue_demo.py

Title: Driving in Shapes using Queues

Author: [PLACEHOLDER] << [Write your name or team name here]

Purpose: [PLACEHOLDER] << [Write the purpose of the script here]

Expected Outcome: Uses queue concept to let the robot drive in a shape after pressing a button
"""

########################################################################################
# Imports
########################################################################################

import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
queue = []
speed = 0
angle = 0

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global queue, speed, angle

    # if A is pressed once, send the instructions to drive in a circle to queue
    if rc.controller.was_pressed(rc.controller.Button.A):
        drive_circle()

    if len(queue) > 0: # if there are instructions in the queue, finish up those instructions
        speed = queue[0][1]
        angle = queue[0][2]

        queue[0][0] -= rc.get_delta_time()

        if queue[0][0] <= 0:
            queue.pop(0)
    else:
        speed = 0
        angle = 0
    rc.drive.set_speed_angle(speed, angle)

def drive_circle(): # adds instructions to the queue asking to drive in a circle
    global queue
    queue.clear()

    CIRCLE_TIME = 5.5
    BRAKE_TIME = 0.5

    queue.append([CIRCLE_TIME, 1, 1])
    queue.append([-1, -1, 1])
    

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
