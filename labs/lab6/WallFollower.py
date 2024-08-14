"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: template.py << [Modify with your own file name!]

Title: Controller Class

Author: [PLACEHOLDER] << [Write your name or team name here]

Purpose: [PLACEHOLDER] << [Write the purpose of the script here]

Expected Outcome: [PLACEHOLDER] << [Write what you expect will happen when you run
the script.]
"""

###########
# IMPORTS #
###########
import sys
sys.path.insert(1, '../../library')
import racecar_utils as rc_utils
import numpy as np
import math

###########################################
# GLOBAL VARIABLES
###########################################
PI = math.pi; SIN = math.sin; COS = math.cos; ARCSIN = math.asin; ATAN2 = math.atan2 
SQRT = math.sqrt; ABS = abs; RAD = math.radians; DEG = math.degrees

degrees_to_rad = RAD
rad_to_degrees = DEG

# Constants
RC = None
speed, angle = 0, 0
Kp = 0.0325
Ki = 0
Kd = 0

####################
# CONTROLLER CLASS #
####################
class WallFollower():
   def __init__(self, racecar):
      global rc
      global speed, angle
      global Kp, Ki, Kd
      rc = racecar
      speed = 0
      angle = 0

   def get_angle_with_wall(self, scans, lidar_range):
      theta1, theta2 = lidar_range
      alpha = theta2 - theta1
      # define both distances
      if theta1 > 180:
         d1 = rc_utils.get_lidar_average_distance(scans, theta2)
         d2 = rc_utils.get_lidar_average_distance(scans, theta1)
      else:
         d1 = rc_utils.get_lidar_average_distance(scans, theta1)
         d2 = rc_utils.get_lidar_average_distance(scans, theta2)

      # if 
      if d1 == 0 or d2 == 0:
         return 0
      
      adjacent = d1*SIN(degrees_to_rad(alpha))
      opposite = d2 - d1*COS(degrees_to_rad(alpha))

      result = rad_to_degrees(ATAN2(opposite, adjacent))
      if theta1 > 180:
         return -result
      return result
      

   def update(self) -> tuple[float, float]: # returns the new speed and angle
      '''
      Takes in the RACECAR's state as a tuple (speed, angle) and returns a tuple (speed, angle) for this current frame's control output.
      '''
      global speed, angle
      global rc
      global error
      global Kp, Ki, Kd
   
      scans = rc.lidar.get_samples()
      # finding angle
      error = self.get_angle_with_wall(scans, (45, 90)) + self.get_angle_with_wall(scans, (270, 315))
      
      if rc.controller.get_trigger(rc.controller.Trigger.RIGHT) > 0:
         speed = 1
      elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) > 0:
         speed = -1
      else:
         speed = 0
      
      angle = rc_utils.clamp(-Kp*error, -1, 1)
            
      return (speed, angle)

   def get_speed(self):
      global speed
      return speed
   
   def get_angle(self):
      global angle
      return angle
   
   def print_error(self):
      global error
      return error
   
