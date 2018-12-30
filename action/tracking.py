# -*- coding: utf-8 -*-

import sys
sys.path.append("../robot/")
from robot import Robot
from TRSensors import TRSensor

my_robot = Robot()
tr = TRSensor()
import time


def tracking(speed):

    position, sensors = tr.readLine()
    l1, l0, m, r0, r1 = sensors
    if max(sensors) - min(sensors) < 300:
        my_robot.setMotor(speed, speed)
    else:
        if min(sensors) == l1:
            my_robot.setMotor(0 * speed, speed)
        elif min(sensors) == l0:
            my_robot.setMotor(0.5 * speed, speed)
        elif min(sensors) == m:
            my_robot.setMotor(speed, speed)
        elif min(sensors) == r0:
            my_robot.setMotor(speed, 0.5 * speed)
        elif min(sensors) == r1:
            my_robot.setMotor(speed, 0 * speed)



if __name__ == '__main__':
    import random
    speed = random.randrange(20, 30)
    
    while True:

        if ((my_robot.left_infrared_status() == False) or (my_robot.right_infrared_status() == False)):
            my_robot.stop()
            speed = random.randrange(20, 30)

        else:
            print('Current speed: {:d}.'.format(speed))
            tracking(speed=speed)
            
        

        
