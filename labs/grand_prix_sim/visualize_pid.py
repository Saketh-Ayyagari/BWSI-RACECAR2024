"""
Saketh Ayyagari
Visualizing PID via graphs using Matplotlib
Can be used for tuning PID values
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

def generateGraph(error_over_time, setpoint):
   # FIRST ARRAY IS LIST OF TIMES, SECOND ARRAY IS ERROR
   plt.plot(error_over_time[0], error_over_time[1])
   plt.plot(error_over_time[0], [setpoint for i in range(len(error_over_time[0]))])
   plt.xlabel("Time (s)")
   plt.ylabel("Error")

   plt.show()

if __name__ == '__main__':
   error_over_time = []
   generateGraph(error_over_time=error_over_time, setpoint=320)