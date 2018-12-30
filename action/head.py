# -*- coding: utf-8 -*-
import sys
sys.path.append("../robot/")
from robot import Robot
import time

my_robot = Robot()

# By defaul, nod or shake 3 times.
def nod_head(n=10):
    my_robot.head_left_right(90)
    time.sleep(0.05)
    print("~ nod head ~")
    for i in range(n):
        my_robot.nod()
    return -1

def shake_head(n=10):
    my_robot.head_up_down(50)
    time.sleep(0.05)
    print("~ shake head ~")
    for i in range(n):
        my_robot.shake()
    return -1

if __name__ == "__main__":
    nod_head()
    shake_head()
