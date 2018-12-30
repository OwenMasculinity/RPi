import sys
sys.path.append("../robot/")
from robot import Robot
import time

my_robot = Robot()

def forward_turn(r=30, l=40, speed=30, mode="left"):
    robot_width = 10
    assert r > robot_width/2
    # Calculate speed.
    iner_speed = ((r - robot_width/2) / float(r)) * speed
    print "iner_speed:"+ str(iner_speed)
    outer_speed = ((r + robot_width/2) / float(r)) * speed
    print "outer_speed:"+ str(outer_speed)
    if mode == "left":
        left_speed = iner_speed
        right_speed = outer_speed
    elif mode == "right":
        left_speed = outer_speed
        right_speed = iner_speed
    else:
        print "Please select direction left or right."
    t = abs(l / float(speed)) * 4
    my_robot.setMotor(left=left_speed, right=right_speed)
    time.sleep(400)
    my_robot.stop()
    return -1
    
    
def pivot_turn(angle=90, speed=50):
    my_robot.setMotor(left=speed,right=-speed)
    t = abs(angle/float(speed)) * 0.9
    time.sleep(t)
    my_robot.stop()

if __name__ == "__main__":
    pivot_turn(angle=90, speed=50)
    forward_turn(r=30, l=40, speed=30,mode="right")

