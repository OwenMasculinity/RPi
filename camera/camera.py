# copy from https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
sys.path.append('../robot/')
from robot import Robot


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

my_robot = Robot()
my_robot.head_up_down(30)


colorLower = (25, 25, 25)
colorUpper = (100, 100, 100)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
 
    # show the frame
    cv2.imshow("Frame", image)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow("mask", mask)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print('center:{0}'.format(center))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            if center[0] <= 280 :
                angle_horizon = my_robot.get_head_angle()[1]
                my_robot.head_left_right(angle_horizon + 5)
                my_robot.left()
            if center[0] >= 360 :
                angle_horizon = my_robot.get_head_angle()[1]
                my_robot.head_left_right(angle_horizon - 5)
                my_robot.right()
            #if center[1] >= 280 :
                 #angle_vertical = my_robot.get_head_angle()[0]
                 #my_robot.head_up_down(angle_vertical - 5)
            #if center[1] <= 200 :
                 #angle_vertical = my_robot.get_head_angle()[0]
                 #my_robot.head_up_down(angle_vertical + 5)
            
    key = cv2.waitKey(1) & 0xFF
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
     
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

camera.close()
cv2.destroyAllWindows()
