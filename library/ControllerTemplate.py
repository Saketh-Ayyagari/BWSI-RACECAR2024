"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: ControllerTemplate.py

Title: Controller Class

Author: Sakth Ayyagari and Stephen Cai

Purpose: Basic Controller Class for organizing outputs such as Line, Lane, and Wall Following

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
      global speed, angle
      rc = racecar
      speed = 0
      angle = 0

   def update(self, current) -> tuple[float, float]: # returns the new speed and angle
      '''
      Takes in the RACECAR's state as a tuple (speed, angle) and returns a tuple (speed, angle) for this current frame's control output.
      '''
      global speed, angle
      
      return (speed, angle)

   def get_speed(self):
      global speed
      return speed
   
   def get_angle(self):
      global angle
      return angle
   
   def clamp(self, value, low, high):
      if value > high:
         return high
      elif value < low:
         return low
      else:
         return value
   
