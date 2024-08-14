"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: two_point_LIDAR.py

Title: Two Point LIDAR Wall Detection

Author: Stephen Cai

Purpose: Detect angle of an adjacent wall relative to the RACECAR
"""

########################################################################################
# Imports
########################################################################################

import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils
import math
import scipy

########################################################################################
# Global variables
########################################################################################

RC = racecar_core.create_racecar()
RC.drive.set_max_speed(0.5)

## Declare any global variables here
# shorten math library names
PI = math.pi
SIN = math.sin
COS = math.cos
ARCSIN = math.asin
ATAN2 = math.atan2
SQRT = math.sqrt
ABS = abs

# tuning values
MAX_INPUT_ANGLE = 1
MAX_DRIVE_ANGLE = 32.0 * PI / 180.0
K_t = 5000
BETA = PI/2
N_RANGES = 3

# other global vars
samples = []


########################################################################################
# Functions
########################################################################################

# [FUNCTION] Gets the distance from a given angle's respective LIDAR sample.
def get_sample(theta):
    rad_per_sample = 2*PI/len(samples)
    new_theta = -theta + PI/2
    new_theta = new_theta % (2*PI)
    index = rc_utils.clamp(round(new_theta/rad_per_sample), 0, len(samples)-1)
    return samples[int(index)]

# [FUNCTION] Gets gamma (wall angle relative to the RACECAR) given the 
# angles of two LIDAR rays, and the LIDAR's distance from the wall.
def get_gamma_distance(theta_range):
    theta_1, theta_2 = theta_range

    # Calculate wall points
    d_1 = get_sample(theta_1)
    d_2 = get_sample(theta_2)

    if d_1==0 or d_2==0:
        # handle out of range measurements
        return (0, 1e9, 1e9)

    x_1, y_1 = (d_1*COS(theta_1), d_1*SIN(theta_1))
    x_2, y_2 = (d_2*COS(theta_2), d_2*SIN(theta_2))

    # Calculate gamma value, subtract from PI/2 to get different from RACECAR heading
    dx = x_1 - x_2
    dy = y_1 - y_2
    gamma = PI/2 - ATAN2(dy, dx)
    gamma = (gamma + 2*PI) % (2*PI) -PI

    # Calculate distance to wall
    m = (y_1 - y_2) / (x_1 - x_2)
    A, B, C = (
        m,
        -1,
        -m*x_1 + y_1
    )
    distance = ABS(C) / SQRT(A**2 + B**2)

    distance_sum = d_1+d_2

    return (gamma, distance, distance_sum)

def get_best_wall(ranges):
    gammas = []
    distances = []
    distance_sums = []
    gamma, distance = (0, 1e9)
    for i in range(len(ranges)):
        wall_gamma, wall_distance, wall_distance_sum = get_gamma_distance(ranges[i])

        if wall_distance < 1e3:
            gammas.append(wall_gamma)
            distances.append(wall_distance)
            distance_sums.append(wall_distance_sum)

    # consider each measurement proportional to its distance significance
    distance_sum_reciprocals = [1/i for i in distance_sums]
    distance_sum_reciprocals_sum = sum(distance_sum_reciprocals)
    distance_props = [i/distance_sum_reciprocals_sum for i in distance_sum_reciprocals]
    
    gamma = sum([gammas[i]*distance_props[i] for i in range(len(gammas))])
    distance = sum([distances[i]*distance_props[i] for i in range(len(distances))])
    
    filtered_distance_sums = list(filter((1e9).__ne__, distance_sums))
    if len(filtered_distance_sums)==0:
        filtered_distance_sums = [1e9]

    # squared to weight the farther walls less
    squared_distance_sum = max(filtered_distance_sums)**2

    return (gamma, distance, squared_distance_sum)


# [FUNCTION] Takes in a LIDAR snapshot and returns angle correction values 
def process_LIDAR(verbose=False):
    global MAX_INPUT_ANGLE, MAX_DRIVE_ANGLE, K_t, BETA, N_RANGES, samples

    ## take in LIDAR snapshot
    samples = RC.lidar.get_samples()

    ## calculate wall values, the clamps are for setting a max error value
    delta_theta = BETA/N_RANGES

    # left
    ranges = [(PI - i*delta_theta, PI - (i+1)*delta_theta) for i in range(N_RANGES)]
    left_gamma, left_distance, left_reciprocal_distance_sum = get_best_wall(ranges)

    # right
    ranges = [(i*delta_theta, (i+1)*delta_theta) for i in range(N_RANGES)]
    right_gamma, right_distance, right_reciprocal_distance_sum = get_best_wall(ranges)

    ## weighting (weight the closer measurement more)
    left_reciprocal_distance_sum = 1/left_reciprocal_distance_sum
    right_reciprocal_distance_sum = 1/right_reciprocal_distance_sum
    reciprocal_sum = left_reciprocal_distance_sum + right_reciprocal_distance_sum

    # multiply by cosine of gamma to give user more control when facing head-on collisions
    left_gamma = rc_utils.clamp(left_gamma, -PI/2, PI/2)
    right_gamma = rc_utils.clamp(right_gamma, -PI/2, PI/2)

    exponent = 1/3
    left_weight = left_reciprocal_distance_sum / reciprocal_sum * COS(left_gamma)**exponent
    right_weight = right_reciprocal_distance_sum / reciprocal_sum * COS(right_gamma)**exponent
    
    # left_weight = COS(left_gamma)
    # right_weight = COS(right_gamma)

    ## calculate correction values
    servo_per_rad = MAX_INPUT_ANGLE / MAX_DRIVE_ANGLE

    # left
    left_denominator = max(1, left_distance**2)
    left_correction = K_t * left_gamma * servo_per_rad / left_denominator
    left_correction = max(0, left_correction)
    left_correction = rc_utils.clamp(left_correction, -MAX_INPUT_ANGLE, MAX_INPUT_ANGLE)
    left_correction *= left_weight

    # right
    right_denominator = max(1, right_distance**2)
    right_correction = K_t * right_gamma * servo_per_rad / right_denominator
    right_correction = min(0, right_correction)
    right_correction = rc_utils.clamp(right_correction, -MAX_INPUT_ANGLE, MAX_INPUT_ANGLE)
    right_correction *= right_weight

    # telemetry
    if verbose:
        print(f"LG {round(left_gamma*180/PI, 2)} | LD {round(left_distance, 2)} | LC {round(left_correction, 2)} ||\nRG {round(right_gamma*180/PI, 2)} | RD {round(right_distance, 2)} | RC {round(right_correction, 2)}\n")
    
    return (left_correction, right_correction)
    

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    pass # Remove 'pass' and write your source code for the start() function here

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    speed = 0
    angle = 0
    
    (lx, ly) = RC.controller.get_joystick(RC.controller.Joystick.LEFT)
    speed += ly
    angle += lx

    if speed >= 0:
        left_correction, right_correction = process_LIDAR(verbose=True)
        angle += right_correction + left_correction

    angle = rc_utils.clamp(angle, -MAX_INPUT_ANGLE, MAX_INPUT_ANGLE)
    RC.drive.set_speed_angle(speed, angle)


# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    pass # Remove 'pass and write your source code for the update_slow() function here


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    RC.set_start_update(start, update, update_slow)
    RC.go()
