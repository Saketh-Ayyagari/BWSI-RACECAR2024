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

###########################################
# IMPORTS #
###########################################
import sys
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils
import numpy as np
import math
from enum import IntEnum

###########################################
# GLOBAL VARIABLES
###########################################
PI = math.pi; SIN = math.sin; COS = math.cos; ARCSIN = math.asin; ATAN2 = math.atan2 
SQRT = math.sqrt; ABS = abs; RAD = math.radians; DEG = math.degrees
###########################################
# Constants
###########################################

BLUE = ((90, 120, 120), (120, 255, 255))  # The HSV range for the color blue
GREEN = ((40, 50, 50), (70, 255, 255))  # The HSV range for the color green
RED = ((0, 150, 150), (10, 255, 255))  # The HSV range for the color red
ORANGE = ((10, 50, 50), (24, 255, 255)) # The HSV range for the color orange
YELLOW = ((24, 70, 70), (30, 255, 255)) # The HSV range for the color yellow
PURPLE = ((125, 50, 50), (165, 255, 255)) # The HSV range for the color purple
PINK = ((90, 150, 150), (179, 230, 255)) # The HSV range for the color pink


MIN_CONTOUR_AREA = 50

rc = None

global speed, angle
speed = 0
angle = 0
global state
global Kp, Ki, Kd
Kp = -0.003325
Ki = 0
Kd = 0

state = None

###########################################
# CONTROLLER AND STATE CLASS #
###########################################

class State(IntEnum):
   L = 0
   R = 1
   LandR = 2

class LaneFollower():
   def __init__(self, racecar):
      global rc, contour_center1, contour_center2
      global state
      rc = racecar
      contour_center1 = None
      contour_center2 = None
      state = None
      global LANE_CROP
      LANE_CROP = ((330, 0), (rc.camera.get_height(), rc.camera.get_width()))

   def update_contours(self): 
      global contour_center1, contour_center2
      global LANE_CROP
      # updating the position of both contour centers and determining which one is on the left or right
      image = rc.camera.get_color_image()
      img = rc_utils.crop(image, LANE_CROP[0], LANE_CROP[1])
      HSV = [ORANGE, PURPLE, PINK]
      
      c = None # unfiltered contours
      # detecting HSV color in order of priority
      for h in HSV:
         x = rc_utils.find_contours(img, h[0], h[1])
         a = rc_utils.get_largest_contour(x)
         if a is not None:
            c = x
            break
      # if any contour is detected
      if c is not None:
         # filter contours
         contours = [x for x in c if rc_utils.get_contour_area(x) > MIN_CONTOUR_AREA] 
         # detects number of contours and organizes them based on which side they're on 
         if len(contours) >= 2:
            center1 = rc_utils.get_contour_center(contours[0])
            center2 = rc_utils.get_contour_center(contours[1])
            if center1[1] < center2[1]:
               contour_center1 = center1
               contour_center2 = center2
            else:
               contour_center2 = center1
               contour_center1 = center2

            
            rc_utils.draw_contour(img, contours[0])
            rc_utils.draw_contour(img, contours[1])

            
            rc_utils.draw_circle(img, contour_center1)
            rc_utils.draw_circle(img, contour_center2)

         elif len(contours) >= 1:
            center = rc_utils.get_contour_center(contours[0])
            rc_utils.draw_contour(img, contours[0])
            rc_utils.draw_circle(img, center)
            if center[1] < 320:
               contour_center1 = center
               contour_center2 = None
            else:
               contour_center2 = center
               contour_center1 = None
      
      image[LANE_CROP[0][0]:LANE_CROP[1][0]][LANE_CROP[0][1]:LANE_CROP[1][1]] = img
      rc.display.show_color_image(image)
      

   def update(self) -> tuple[float, float]: # returns the new speed and angle
      global speed, angle
      global contour_center1, contour_center2
      global state
      
      self.update_contours()

      # deciding the state of state machine
      if contour_center1 is not None and contour_center2 is not None:
         state = State.LandR
      elif contour_center1 is not None and state != State.R:
         state = State.L
      elif contour_center2 is not None and state != State.L:
         state = State.R

      # deciding angle based on state
      if state == State.L:
         angle = 1
      elif state == State.R:
         angle = -1   
      else:
         SETPOINT = 320
         error = SETPOINT - (contour_center1[1] + contour_center2[1])//2
         angle = rc_utils.clamp(Kp*error, -1, 1)

      
      return (speed, angle)

   def get_state(self):
      global state
      return state
   