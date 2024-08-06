"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab6.py

Title: Lab 6 - Wall Follower

Author: [PLACEHOLDER] << [Write your name or team name here]

GRAND PRIX SIMULATOR CODE
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
import math
import racecar_core
import racecar_utils as rc_utils
from enum import IntEnum

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()
rc.drive.set_max_speed(0.5)
# Declare any global variables here
global speed, angle, state
global scans
speed = 0
angle = 0
state = None
Kp = 0; Ki = 0; Kd = 0
# FOR I and D parts 
int_sum = 0
prevError = None
# Detecting AR ID Markers
ar_id = None

class State(IntEnum):
    L = 0 # Only left wall is visible
    R = 1 # Only right wall is visible
    LandR = 2 # Both walls are visible

PI = math.pi; SIN = math.sin; COS = math.cos; ARCSIN = math.asin; ATAN2 = math.atan2 
SQRT = math.sqrt; ABS = abs; RAD = math.radians; DEG = math.degrees

########################################################################################
# Functions
########################################################################################
def camera():
    global ar_id
    image = rc.camera.get_color_image()
    ar_markers = rc_utils.get_ar_markers(image)

    if len(ar_markers) > 0:
        ar_id = ar_markers[0].get_id()
    rc_utils.draw_ar_markers(image, ar_markers)

    rc.display.show_color_image(image)


# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed, angle
    global Kp, Ki, Kd
    
    speed = 0
    angle = 0
    
    # NOTE: PID Values for default speed (~1 m/s)
    # Kp = 0.071
    # Ki = 0
    # Kd = 0.00083

    Kp = 0.035
    Ki = 0#.003125
    Kd = 0.0013
    rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global speed, angle
    global left, right
    global Kp, Ki, Kd
    global state
    
    global scans, error
    global P_error, D_error
    global int_sum
    global prevError

    global ar_id
    
    camera()

    speed = 0.75
    scans = rc.lidar.get_samples()
    '''
    ALWAYS USE LOOK AHEAD TO COMPENSATE FOR LAG. NO SYSTEM IS GOING TO BE PERFECT!!!!!!!!!!
    '''
    left = rc_utils.get_lidar_closest_point(scans, (290, 305))[1]
    right = rc_utils.get_lidar_closest_point(scans, (55, 70))[1]


    # if rc.controller.get_trigger(rc.controller.Trigger.RIGHT) > 0:
    #     speed = 1
    # elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) < 0:
    #     speed = -1
    # else:
    #     speed = 0
      
    # (angle, y) = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    
    if left != 0 and right != 0:
        state = State.LandR
    elif right != 0:
        state = State.R
    elif left != 0:
        state = State.L

    if ar_id == 2:
        state = State.R
    
    SETPOINT = 100
    D_error = 0
    
    if state == State.L:
        error = SETPOINT - left
        P_error = Kp*error
                
    elif state == State.R:
        error = SETPOINT - right
        P_error = -Kp*error
    
    elif state == State.LandR:
        setpoint = (left + right)/2
        error = setpoint - left
        P_error = Kp*error
    # calculating integral error
    int_sum+=(rc.get_delta_time() * error)
    I_error = Ki*int_sum
    # calculating derivative error
    if prevError is not None:
        D_error = Kd*(error-prevError/rc.get_delta_time())
        
    angle = rc_utils.clamp(P_error + I_error + D_error, -1, 1)
    
    
    prevError = error

    
    rc.drive.set_speed_angle(speed, angle)

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    global speed, angle
    global left, right
    global Kp, Ki, Kd
    global state
    global error_log
    global scans, error
    global P_error, D_error
    global ar_id

    print(f"State: {state}")
    print(f"Error: {error} | Angle: {angle}")
    print(f"Left: {left} | Right: {right}")
    print(f"P-error: {P_error} | D-error: {D_error}")
    print(f"AR ID: {ar_id}")
    print('='*60)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()


