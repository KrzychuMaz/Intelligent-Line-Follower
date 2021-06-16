from controller import Robot
from controller import Camera
from controller import DistanceSensor, Motor
import time
import cv2
import numpy as np
import sys
from controller import Display

def run_robot(robot):
    time_step = 32
    #max_speed = 0
    step = -1
    
    #camera
    camera = Camera('camera1')
    camera.enable(time_step)

    #motors
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    
    #irsensors
    left_ir = robot.getDevice('ir0')
    left_ir.enable(time_step)
    
    right_ir = robot.getDevice('ir1')
    right_ir.enable(time_step)
     
    # Step simulation
    while robot.step(time_step) != -1:
    
        left_ir_value = left_ir.getValue()
        right_ir_value = right_ir.getValue()
        
        camera.saveImage("cam.png", 20)
        icv = cv2.imread("cam.png")
        imCrop = icv[ 0:640, 0:640]
        bw = icv[ 0:640, 0:640]
        width = camera.getWidth()
        height = camera.getHeight()
        x1, y1 = 318, 0
        x2, y2 = 318, 640
        cv2.line(imCrop, (x1, y1), (x2, y2), (0, 0, 255), thickness=4)
        (thresh, blackAndWhiteImage) = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite( 'bw.png', blackAndWhiteImage) 
        bwcount = cv2.imread("bw.png", 0)
        left_px = bwcount[:, 0:319]
        right_px = bwcount[:, 320:640]
        
        left_black = 204160- cv2.countNonZero(left_px)
        right_black = 204800 - cv2.countNonZero(right_px)
        print ("Black px on left: ", left_black, " on right px: ", right_black)
       
       
        if(right_black+left_black==0):
            max_speed = 1.5
        elif((right_black==0) or (left_black==0)):
            max_speed = 2
        else:
            max_speed = 6.28
            
        left_speed = max_speed 
        right_speed = max_speed
        
        if (left_ir_value > right_ir_value) and (6 < left_ir_value < 15):
            left_speed = -max_speed
        elif (right_ir_value > left_ir_value) and (5 < right_ir_value < 15):
            right_speed = -max_speed
        
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
        print("Speed: ", max_speed)
    
if __name__ == "__main__":
    
    my_robot = Robot()
    run_robot(my_robot)