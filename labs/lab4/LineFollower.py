"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: template.py << [Modify with your own file name!]

Title: Segment Optimizer

Author: [PLACEHOLDER] << [Write your name or team name here]

Purpose: [PLACEHOLDER] << [Write the purpose of the script here]

Expected Outcome: [PLACEHOLDER] << [Write what you expect will happen when you run
the script.]
"""

###########
# IMPORTS (BOTH CLASSES AND MODULES) #
###########
import sys
sys.path.insert(1, '../../library') # inserts a path for finding modules
import racecar_core
import racecar_utils as rc_utils
import numpy as np
import math
import cv2 as cv

from ControllerTemplate import Controller

###########################################
# GLOBAL VARIABLES
###########################################
PI = math.pi; SIN = math.sin; COS = math.cos; ARCSIN = math.asin; ATAN2 = math.atan2 
SQRT = math.sqrt; ABS = abs; RAD = math.radians; DEG = math.degrees

# Constants
rc = None
global speed, angle
global Kp, Ki, Kd
Kp = 0.003125
Ki = 0.001
Kd = 0.0003

error_sum = 0
time = []
error = []

# Previous error for derivative
prevError = None
# cumulative error for integral
sum = 0
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 55


# TODO Part 1: Determine the HSV color threshold pairs for BLUE, GREEN, and RED

BLUE = ((80, 100, 50), (120, 255, 255))  # The HSV range for the color blue
GREEN = ((40, 150, 150), (80, 255, 255))  # The HSV range for the color green
RED = ((0, 50, 50), (10, 255, 255))  # The HSV range for the color red

WHITE = ((0, 60, 150), (179, 70, 255)) # The HSV range for the color white
YELLOW = ((20, 0, 25), (40, 255, 255)) # The HSV range for the color yellow
PURPLE = ((125, 50, 25), (165, 255, 255)) # The HSV range for the color purple
BLACK = ((0, 50, 0), (179, 255, 56)) # The HSV range for the color black
ORANGE = ((10, 50, 50), (20, 255, 255)) # The HSV range for the color orange
PINK = ((90, 150, 150), (179, 230, 255)) # The HSV range for the color pink

# Color priority: Red >> Green >> Blue
COLOR_PRIORITY = None
# All possible color priorities
COLOR_PRIORITY_WHITE = (RED, GREEN, BLUE)
COLOR_PRIORITY_PURPLE = (BLUE, RED, GREEN)
COLOR_PRIORITY_YELLOW = (RED, BLUE, GREEN)
COLOR_PRIORITY_ORANGE = (BLUE, GREEN, RED)
COLOR_PRIORITY_BLACK = (GREEN, RED, BLUE)
COLOR_PRIORITY_PINK = (GREEN, BLUE, RED)


########################################
# CONTROLLER CLASS 
########################################
class LineFollower(Controller):
   def __init__(self, racecar):
      global rc
      global speed, angle
      global COLOR_PRIORITY
      global CROP_FLOOR
      rc = racecar
      speed = 0
      angle = 0
      self.contour_center = None
      self.contour_area = 0
      COLOR_PRIORITY = (RED, GREEN, BLUE)
      CROP_FLOOR = ((330, 0), (rc.camera.get_height()-20, rc.camera.get_width())) # crop floor for line detection


   def update_contour(self):
      global rc
      global contour_center, contour_area
      global COLOR_PRIORITY, CROP_FLOOR
      image = rc.camera.get_color_image()
      # # gets AR markers
      # ar_markers = rc_utils.get_ar_markers(image)
      # if len(ar_markers) > 0:
      #    rc_utils.draw_ar_markers(image, ar_markers)
      #    if (ar_markers[0].get_id() == 32):
      #       rc.drive.set_max_speed(0.25)
      #    else:
      #       rc.drive.set_max_speed(0.47)

      # A crop window for the floor directly in front of the car
      
      # TODO Part 2: Complete this function by cropping the image to the bottom of the screen,
      # analyzing for contours of interest, and returning the center of the contour and the
      # area of the contour for the color of line we should follow (Hint: Lab 3)

      line_img = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

      contours = None
      for c in COLOR_PRIORITY:
         contour_list = rc_utils.find_contours(line_img, c[0], c[1])
         center = rc_utils.get_contour_center(rc_utils.get_largest_contour(contour_list, MIN_CONTOUR_AREA))
         if center is not None:
            contours = contour_list
            break    
      if contours is not None:
         desired_contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)       
         self.contour_center = rc_utils.get_contour_center(desired_contour)
         self.contour_area = cv.contourArea(desired_contour)
         cv.circle(line_img, (self.contour_center[1], self.contour_center[0]), 4, (255, 255, 0), -1)
         cv.drawContours(line_img, [c for c in contours if cv.contourArea(c) > MIN_CONTOUR_AREA]
                           , -1, (255, 255, 0), 2)
      else: # if there are no contours, then set contour area = 0 and contour center = None
      # Doing this prevents integrator windup since there is no extra error being calculated or summed up
         self.contour_area = 0
         self.contour_center = None
         
      # cv.circle(image, (rc.camera.get_width()//2, rc.camera.get_height()//2), 6, (255, 0, 255), -1)

      image[CROP_FLOOR[0][0]:CROP_FLOOR[1][0], 
            CROP_FLOOR[0][1]:CROP_FLOOR[1][1]] = line_img
      
      rc.display.show_color_image(image)

   def update(self) -> tuple[float, float]: # returns the new speed and angle
      '''
      Takes in the RACECAR's state as a tuple (speed, angle) and returns a tuple (speed, angle) for this current frame's control output.
      '''
      global rc
      global speed, angle
      global contour_area, contour_center
      global COLOR_PRIORITY
      global Kp, Ki, Kd
      global prevError
      global error_sum # for integral term
      global P, I, D

      self.update_contour()

      # keeps error the same if there is no contour_center visible
      # also prevents integrator windup
      if self.contour_center is not None: 
         error = (rc.camera.get_width() // 2) - self.contour_center[1]
         P = -Kp*error
         D = 0
         if prevError is not None:
            D = -Kd * ((error - prevError)/rc.get_delta_time())
         error_sum+=error*rc.get_delta_time()
         I = error_sum*-Ki
         
         prevError = error
         angle = rc_utils.clamp(P + I + D, -1, 1)

    # TODO Part 4: Determine the speed that the RACECAR should drive at. This may be static or
    # variable depending on the programmer's intent.
         speed = 1
      
      return (speed, angle)
   
   def get_center(self):
      return self.contour_center
   
   def get_area(self):
      return self.contour_area
   
   def get_P_error(self):
      global P
      return P
   def get_I_error(self):
      global I
      return I
   def get_D_error(self):
      global D
      return D