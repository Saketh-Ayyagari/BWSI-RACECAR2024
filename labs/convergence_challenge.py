"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: Convergence Challenge

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
sys.path.insert(1, '../library')
import numpy as np
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()
# Declare any global variables here
speed = 0
angle = 0

data = []

########################################################################################
# Functions
########################################################################################
def calculate_rolling_avg(data, N): 
    r_avg = []
    temp_avg = []

    for i in range(len(data)):
        if i < N-1:
            r_avg.append(data[i])
            temp_avg.insert(0, data[i])
        else:
            temp_avg.insert(0, data[i])
            temp_sum = sum(temp_avg[0:N])
            r_avg.append(temp_sum/N)
    return r_avg[-1]

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed, angle
    speed = 0
    angle = 0
    rc.set_update_slow_time(0.125)

    rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global data, distance
    scans = rc.lidar.get_samples()
    _, distance = rc_utils.get_lidar_closest_point(scans, (355, 5))
    # appends distance to data and calculates rolling average
    data.append(distance)
    distance = calculate_rolling_avg(data, N=3)
    acceleration = rc.physics.get_linear_acceleration()[2]
    if distance < 30+108:
        speed = 0
    else:
        speed = 1
    
    
        
    rc.drive.set_speed_angle(speed, angle)
# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    print(f"Front distance: {distance} cm")

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
