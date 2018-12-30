# -*- coding: utf-8 -*-
import sys

sys.path.append("../robot/")

from robot import Robot
from turn import forward_turn, pivot_turn
from head import nod_head,shake_head
import time

def dance_mode_1():
    forward_turn(r=50, l=10, speed=30,mode="left")
    forward_turn(r=50, l=10, speed=30,mode="right")
    forward_turn(r=50, l=10, speed=-30,mode="left")
    forward_turn(r=50, l=10, speed=-30,mode="right")
    pivot_turn(angle=180, speed=50)
    nod_head()
    return -1

def dance_mode_2():
    forward_turn(r=50, l=10, speed=30,mode="left")
    forward_turn(r=50, l=10, speed=30,mode="right")
    forward_turn(r=50, l=10, speed=-30,mode="left")
    forward_turn(r=50, l=10, speed=-30,mode="right")
    pivot_turn(angle=180, speed=50)
    shake_head()
    return -1

def dance(mode=2):
    if mode == 1:
        dance_mode_1()
    elif mode == 2:
        dance_mode_2()
    else:
        print("Please select dance mode.")
    return -1

if __name__ == "__main__":
    dance()

    
