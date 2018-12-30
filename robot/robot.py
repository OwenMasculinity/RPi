import RPi.GPIO as GPIO
import time
import math
from PCA9685 import PCA9685

class Robot(object):
	
    def __init__(self,ain1=12,ain2=13,ena=6,bin1=20,bin2=21,enb=26,dr=16,dl=19):
        # for wheels
        self.AIN1 = ain1
        self.AIN2 = ain2
        self.BIN1 = bin1
        self.BIN2 = bin2
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.AIN1,GPIO.OUT)
        GPIO.setup(self.AIN2,GPIO.OUT)
        GPIO.setup(self.BIN1,GPIO.OUT)
        GPIO.setup(self.BIN2,GPIO.OUT)
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.ENB,GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

        # for head motors
        self.PWMC = PCA9685(0x40, debug=True)
        self.PWMC.setPWMFreq(50)
        self.ANGLE_HORZN = 90     # ANGLE_HORZN in [0, 180]
        self.ANGLE_VERTC = 90     # ANGLE_VERTC in [0, 150]
        self.head_reset()
        
        # for infrared sensors
        self.DR = dr
        self.DL = dl
        GPIO.setup(self.DR,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.DL,GPIO.IN,GPIO.PUD_UP)

    def forward(self):
        print('forward')
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.HIGH)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.HIGH)
        
    def stop(self):
        print('stop')
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.LOW)
        
    def backward(self):
        print('backward')
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1,GPIO.HIGH)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.HIGH)
        GPIO.output(self.BIN2,GPIO.LOW)
	
    def left(self):
        print('left')
        self.PWMA.ChangeDutyCycle(5)
        self.PWMB.ChangeDutyCycle(5)
        GPIO.output(self.AIN1,GPIO.HIGH)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.HIGH)
        time.sleep(0.002)

    def right(self):
        print('right')
        self.PWMA.ChangeDutyCycle(5)
        self.PWMB.ChangeDutyCycle(5)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.HIGH)
        GPIO.output(self.BIN1,GPIO.HIGH)
        GPIO.output(self.BIN2,GPIO.LOW)
        time.sleep(0.002)
		
    def setPWMA(self,value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def setPWMB(self,value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)	
		
    def setMotor(self, left, right):

        if((right >= 0) and (right <= 100)):
            GPIO.output(self.BIN1,GPIO.LOW)
            GPIO.output(self.BIN2,GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(right)
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.BIN1,GPIO.HIGH)
            GPIO.output(self.BIN2,GPIO.LOW)
            self.PWMB.ChangeDutyCycle(0 - right)

        if((left >= 0) and (left <= 100)):
            GPIO.output(self.AIN1,GPIO.LOW)
            GPIO.output(self.AIN2,GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(left)
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.AIN1,GPIO.HIGH)
            GPIO.output(self.AIN2,GPIO.LOW)
            self.PWMA.ChangeDutyCycle(0 - left)

    def left_infrared_status(self):
        status = GPIO.input(self.DR)
        print('left infrared sensor:{0}'.format(status))
        return status

    def right_infrared_status(self):
        status = GPIO.input(self.DL)
        print('right infrared sensor:{0}'.format(status))
        return status

    def angle2int(self, angle, channel):
        assert channel == 0  or channel == 1
        if channel == 0:
            return int(1500 + ( angle - 90 ) * 10)
        else:
            return int(1700 + ( angle - 90 ) * 10)

    def head_reset(self):
        self.ANGLE_HORZN = 90     
        self.ANGLE_VERTC = 90
        self.PWMC.setServoPulse(0,1500)
        time.sleep(0.02)
        self.PWMC.setServoPulse(1,1700)
        time.sleep(0.02)
        

    def get_head_angle(self):
        print('head angle: [{0}, {1}]'.format(self.ANGLE_HORZN, self.ANGLE_VERTC))
        return [self.ANGLE_HORZN, self.ANGLE_VERTC]

    def head_left_right(self, angle):
        assert 0 <= angle and angle <= 180
        self.ANGLE_HORZN = angle
        print('head horizontal angle:{0}'.format(self.ANGLE_HORZN))
        self.PWMC.setServoPulse(0,self.angle2int(angle, 0))
        time.sleep(0.02)

    def head_up_down(self, angle):
        assert 0 <= angle and angle <= 150
        self.ANGLE_VERTC = angle
        print('head vertical angle:{0}'.format(self.ANGLE_VERTC))
        self.PWMC.setServoPulse(1,self.angle2int(angle, 1))
        time.sleep(0.02)

    def nod(self, angle_lower=70, angle_higher=30, org_horzn=90):

        self.head_up_down(angle_lower)
        time.sleep(0.1)
        self.head_up_down(angle_higher)
        time.sleep(0.1)
        self.stop()

    def shake(self, angle_left=115, angle_right=75):
        self.head_left_right(angle_left)
        time.sleep(0.1)
        self.head_left_right(angle_right)
        time.sleep(0.1)
        self.stop()

    def head_left_right_rotate(self, end_angle, step=3):
        assert 0 <= end_angle and end_angle <= 180
        start_angle=self.ANGLE_HORZN
        if end_angle < start_angle:
            step = -step
        for angle in range(start_angle,end_angle, step):
            self.head_left_right(angle)
        print("finished.")

if __name__=='__main__':
    
    my_robot = Robot()

    for angle in range(0, 180):
        my_robot.head_left_right(angle)

    for angle in range(0, 150):
        my_robot.head_up_down(angle)

    for i in range(1, 100):
        my_robot.forward()

    for i in range(1, 100):
        my_robot.backward()

    for i in range(1, 100):
        my_robot.left()

    for i in range(1, 100):
        my_robot.right()
    
    for i in range(1, 100):
        my_robot.right_infrared_status()
        my_robot.left_infrared_status()
        
    my_robot.stop()

