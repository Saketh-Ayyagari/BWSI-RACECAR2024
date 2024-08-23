"""
This program does a simple SLAM 
"""

import numpy as np
import cv2 as cv
import sys
import math
import matplotlib.pyplot as plt

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils


########################################################################################
# Global variables
########################################################################################
rc = racecar_core.create_racecar()

rad_to_degrees = math.degrees
degrees_to_rad = math.radians
floor = math.floor
# trig functions are in radians
cos = math.cos
sin = math.sin
π = math.pi
global speed, angle
CAR_POSITION = (rc.camera.get_height()//2, rc.camera.get_width()//2)


def update_point_map():
   global scans
   scans = rc.lidar.get_samples()
   image = rc.camera.get_color_image()

   rc_utils.draw_circle(image, CAR_POSITION, (0, 0, 255))
   for a in range(360):
      distance = rc_utils.get_lidar_average_distance(scans, a)

      if distance > 0:
         # using sin and cos to break up the distance into components
         vertical_distance = distance*cos(degrees_to_rad(a))
         horizontal_distance = distance*sin(degrees_to_rad(a))
         # plotting each point of the lidar map
         point = (CAR_POSITION[0] - rc_utils.clamp(floor(vertical_distance*0.3), -CAR_POSITION[0]+1, CAR_POSITION[0]), 
                  CAR_POSITION[1] + rc_utils.clamp(floor(horizontal_distance*0.3), -CAR_POSITION[1], CAR_POSITION[1]-1))
         rc_utils.draw_circle(image, point, (0, 255, 0), radius=3)
         
   rc.display.show_color_image(image)

def generate_map():
   graph = np.zeros((480, 640, 3)) # in RGB format
   graph[CAR_POSITION[0]][CAR_POSITION[1]] = np.array([255, 0, 0])
   scans = rc.lidar.get_samples()

   for a in range(360):
      distance = rc_utils.get_lidar_average_distance(scans, a)

      if distance > 0:
         # using sin and cos to break up the distance into components
         vertical_distance = distance*cos(degrees_to_rad(a))
         horizontal_distance = distance*sin(degrees_to_rad(a))
         # plotting each point of the lidar map
         point = (CAR_POSITION[0] - rc_utils.clamp(floor(vertical_distance*0.3), -CAR_POSITION[0]+1, CAR_POSITION[0]), 
                  CAR_POSITION[1] + rc_utils.clamp(floor(horizontal_distance*0.3), -CAR_POSITION[1], CAR_POSITION[1]-1))
         

   plt.imshow(graph)
   plt.show()

def start():
   global speed, angle
   speed = 0
   angle = 0

   rc.drive.stop()

def update():
   global speed, angle
   global scans
   update_point_map()

   right = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
   left = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
   if right > 0:
      speed = right
   elif left > 0:
      speed = -left
   else:
      speed = 0

   angle, __ = rc.controller.get_joystick(rc.controller.Joystick.LEFT)


   # Send the speed and angle values to the RACECAR
   rc.drive.set_speed_angle(speed, angle)



if __name__ == '__main__':
   rc.set_start_update(start, update)
   rc.go()