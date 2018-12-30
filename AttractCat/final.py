# copy from https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# import the necessary packages
# -*- coding: utf-8 -*-
import sys
sys.path.append("../robot/")
from robot import Robot
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import RPi.GPIO as GPIO
from AlphaBot import AlphaBot
import numpy as np
import os
import pygame  # pip install pygame
import threading

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
    time.sleep(t)
    my_robot.stop()
    return -1
    
    
def pivot_turn(angle=90, speed=50):
    my_robot.setMotor(left=speed,right=-speed)
    t = abs(angle/float(speed)) * 0.9
    time.sleep(t)
    my_robot.stop()


def recognise():
    my_robot.head_up_down(90)
    my_robot.head_left_right(60)
    ### Setup #####################################################################
     
    # Center coordinates
    cx = 160
    cy = 120
     
    os.system( "echo 0=150 > /dev/servoblaster" )
    os.system( "echo 1=150 > /dev/servoblaster" )
     
    xdeg = 150
    ydeg = 150
     
    # Setup the camera
    camera = PiCamera()
    camera.resolution = ( 320, 240 )
    camera.framerate = 60
    rawCapture = PiRGBArray( camera, size=( 320, 240 ) )
     
    # Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier( '/home/pi/Downloads/opencv-2.4.9/data/lbpcascades/lbpcascade_frontalface.xml' ) 
     
    t_start = time.time()
    fps = 0
     
     
    ### Main ######################################################################
     
    # Capture frames from the camera
    for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
     
        image = frame.array
     
        # Use the cascade file we loaded to detect faces
        gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
        faces = face_cascade.detectMultiScale( gray )
     
        print "Found " + str( len( faces ) ) + "face(s)"
        print faces
        # Draw a rectangle around every face and move the motor towards the face
        for ( x, y, w, h ) in faces:
     
            cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 100, 255, 100 ), 2 )
            cv2.putText( image, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
     
            tx = x + w/2
            ty = y + h/2

            

            # if   ( cx - tx >  10 and xdeg <= 190 ):
                # xdeg += 3
                # os.system( "echo 0=" + str( xdeg ) + " > /dev/servoblaster" )
            # elif ( cx - tx < -10 and xdeg >= 110 ):
                # xdeg -= 3
                # os.system( "echo 0=" + str( xdeg ) + " > /dev/servoblaster" )
     
            # if   ( cy - ty >  10 and ydeg >= 110 ):
                # ydeg -= 3
                # os.system( "echo 1=" + str( ydeg ) + " > /dev/servoblaster" )
            # elif ( cy - ty < -10 and ydeg <= 190 ):
                # ydeg += 3
                # os.system( "echo 1=" + str( ydeg ) + " > /dev/servoblaster" )
        if len( faces ) == 1:
            if tx <= 110 :
                angle_horizon = my_robot.get_head_angle()[0]
                my_robot.head_left_right(angle_horizon + 5)
                my_robot.right()
            if tx >= 210 :
                angle_horizon = my_robot.get_head_angle()[0]
                my_robot.head_left_right(angle_horizon - 5)
                my_robot.left()
            if tx <= 190 & tx >= 130:
                break 
        # Calculate and show the FPS
        fps = fps + 1
        sfps = fps / ( time.time() - t_start )
        cv2.putText( image, "FPS : " + str( int( sfps ) ), ( 10, 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )    
     
        # Show the frame
        cv2.imshow( "Frame", image )
        cv2.waitKey( 1 )
         # Clear the stream in preparation for the next frame
        rawCapture.truncate( 0 )

    camera.close()
    cv2.destroyAllWindows()

def infrared_stop():   
    try:
            while True:
                    DR_status = GPIO.input(16)
                    DL_status = GPIO.input(19)
                    if((DL_status == 1) and (DR_status == 1)):
                            my_robot.forward()
                            print("forward")
                    elif((DL_status == 1) and (DR_status == 0)):
                            my_robot.left()
                            print("left")
                    elif((DL_status == 0) and (DR_status == 1)):
                            my_robot.right()
                            print("right")
                    else:
                            my_robot.backward()
                            time.sleep(0.2)
                            my_robot.stop()
                            print("backward")
                            break

    except KeyboardInterrupt:
            GPIO.cleanup();

def nod_head(n=5):
    my_robot.head_left_right(90)
    time.sleep(0.05)
    print("~ nod head ~")
    for i in range(n):
        my_robot.nod()
    return -1

def shake_head(n=5):
    my_robot.head_up_down(60)
    time.sleep(0.05)
    print("~ shake head ~")
    for i in range(n):
        my_robot.shake()
    return -1




def playMusic(filename, loops=0, start=0.0, value=0.5):
  
    flag = False 
    pygame.mixer.init()
    # while 1:
    if flag == 0:
        pygame.mixer.music.load(filename)
            # pygame.mixer.music.play(loops=0, start=0.0) loopsºÍstart·ֱð´ú±íÖظ´µĴÎÊýºͿªʼ²¥·ŵÄλÖá£
            # pygame.mixer.music.play(loops=loops, start=start)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(value)  
        # if pygame.mixer.music.get_busy() == True:
            # flag = True
        # else:
            # if flag:
                # pygame.mixer.music.stop()  
                # break



#playMusic('out.wav')
if __name__ == "__main__":
    recognise() # recognise cat
    infrared_stop() # walk to cat and stop
    nod_head()
    shake_head()
    
    # music_thread=threading.Thread(target=playMusic('1.mp3'),name='music_thread')
    # music_thread.start()
    # music_thread.join()
    playMusic('lisinan.mp3')
    pivot_turn(angle=90, speed=50)
    pivot_turn(angle=90, speed=50) 
    forward_turn(r=30, l=40, speed=30,mode="right")
    forward_turn(r=30, l=40, speed=30,mode="left")
    my_robot.stop()
    pygame.mixer.music.stop()
    
    recognise() # recognise cat
    infrared_stop() # walk to cat and stop
    nod_head()
    shake_head()
    playMusic('1.mp3')
    pivot_turn(angle=90, speed=50)
    pivot_turn(angle=90, speed=50) 
    forward_turn(r=30, l=40, speed=30,mode="right")
    forward_turn(r=30, l=40, speed=30,mode="left")   
    my_robot.stop()  
    
        
    

