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

# Constants
RC = None

####################
# CONTROLLER CLASS #
####################
class Controller():
   def __init__(self, racecar):
      global rc
      rc = racecar

   def update(self, current) -> tuple[float, float]: # returns the new speed and angle
      '''
      Takes in the RACECAR's state as a tuple (speed, angle) and returns a tuple (speed, angle) for this current frame's control output.
      '''
      speed, angle = current
      return (speed, angle)

   def get_speed(self):
      global speed
      return speed
   def get_angle(self):
      global angle
      return angle
   