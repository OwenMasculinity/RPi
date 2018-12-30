# -*- coding: utf-8 -*-
import sys
sys.path.append("../robot/")
from robot import Robot
import time

my_robot = Robot()

def move(speed=30, consider_obstacle=True, duration=None):
    if duration != None:
        consider_obstacle = False
    if speed>0 and consider_obstacle:
        flag = True
        while flag:
            if my_robot.left_infrared_status() and my_robot.right_infrared_status():
                my_robot.setMotor(speed,speed)
            else:
                my_robot.stop()
                flag = False
                print "There is obstacle in front of me!"
    else:
        my_robot.setMotor(speed,speed)
        time.sleep(duration)
        my_robot.stop()


if __name__ == "__main__":
    # move(speed=30,duration=3)

    move(speed=30)
    
    
