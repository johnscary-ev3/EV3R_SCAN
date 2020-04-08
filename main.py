#!/usr/bin/env pybricks-micropython

#Modified to include just Scan Head Object Detect functions Apr 7, 2020
#Modified to work with EV3 micro-python Rev3  Mar 30, 2020
#Modified for EV3RSTORM ; started Feb 18 2020
#RC Mode, Detect objects and Ambient Light, Gyro turns, Check directions or Random reverse or Run blades on detect object modes

#KRAZ3 modified with Scan Head to get directions  Jan 9 2020
#KRAZ3_RC_SCAN_HEAD Project

#from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
brick =EV3Brick()

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from threading import Thread

import motion_tools
import object_tools
import sound_tools


#Hardware Configuration Flags 
UltrasonicPresent =True
UltrasonicPresent_2 =True

ScanHeadPresent = True
ScanHeadHomeRight = True

ScanHeadPresent_2 = True
ScanHeadHomeRight_2 = False

#Scanhead offset from home to forward position
ScanHeadHomeOffset = -55
ScanHeadHomeOffset_2 =  90

#Ports for Sensor Inputs
InfraredSensorPort = Port.S4
object_tools.UltrasonicSensorPort =Port.S2
object_tools.UltrasonicSensorPort_2 =Port.S3

#Config variables
UseScanHeadObjectDetect = True
object_tools.object_detect_sound_on = True

#variables used later
buttons=[]

#  All  Head directions
#target_angle = [-90, -45, 0, 45, 90, 135, 180, 225]
#target_direc = [  6,   7, 0,  1,  2,   3,   4,   5]
#num_head_poistions =8

# Scan Head direction subset used for Initialization
target_angle = [-45, 0, 45]
target_direc = [  7, 0,  1]
num_head_poistions =3


# Play a sound.
brick.speaker.beep(500, 100)

 # Turn the light green
brick.light.on(Color.GREEN)

# Set Display
#brick.display.image(ImageFile.EV3)
brick.screen.load_image(ImageFile.EV3)

#Init the Ultrasonic Distance sensors
if UltrasonicPresent:
    object_tools.Init_UltrasonicSensor()
if UltrasonicPresent_2:
    object_tools.Init_UltrasonicSensor_2()

#Init Small Motors if present
if ScanHeadPresent :
    motion_tools.Init_MotorA()
if ScanHeadPresent_2 :
    motion_tools.Init_MotorD()

#set up some motor speeds
head_speed = 300

# Init the Scan Head
if ScanHeadPresent:
    motion_tools.init_scan_head(head_speed, ScanHeadHomeRight, ScanHeadHomeOffset)
    #  Test head directions
    for i in range(num_head_poistions):
        motion_tools.move_scan_head_target(head_speed, target_angle[i])
        motion_tools.direction_sound(target_direc[i], False)
        wait(250)
    #Reset head to 0 position
    motion_tools.move_scan_head_target(head_speed, 0)

# Init the Scan Head 2
if ScanHeadPresent_2:
    motion_tools.init_scan_head_2(head_speed, ScanHeadHomeRight_2, ScanHeadHomeOffset_2)
     #  Test head directions
    for i in range(num_head_poistions):
        motion_tools.move_scan_head_target_2(head_speed, target_angle[i])
        motion_tools.direction_sound(target_direc[i], False)
        wait(250)
    #Reset head to 0 position
    motion_tools.move_scan_head_target_2(head_speed, 0)

# Play another beep sound.
# This time with a higher pitch (1000 Hz) and longer duration (500 ms).
brick.speaker.beep(1000, 500)

# Initialize IR sensors
ir =InfraredSensor(InfraredSensorPort)

#Start object detect and sound threads
if UltrasonicPresent:
        object_tools.object_detect_run= True
if UltrasonicPresent_2:
        object_tools.object_detect_run_2 = True

object_tools.start_object_detect()
object_tools.start_object_sound_thread()


#Start Up Scan heads move Loop
if UseScanHeadObjectDetect:
    if ScanHeadPresent:
        motion_tools.scan_head_move = True
    if ScanHeadPresent_2:
        motion_tools.scan_head_move_2 = True
    if (ScanHeadPresent or ScanHeadPresent_2):
        motion_tools.scan_head_speed = head_speed
        motion_tools.start_scan_head_thread()

# Main loop 
# Will exit based on Exit Button

#Set some Control Flags
main_loop = True
butt_len1 = 0
butt_len2 = 0
butt_len3 = 0
butt_len4 = 0
direction = 0

while main_loop ==True:
    
    #print some staus info
    print(" ")
    print("dist=", object_tools.dist, "mm","    dist_2=", object_tools.dist_2, "mm")
    print("object_detected=", object_tools.object_detected, "object_detected_1=", object_tools.object_detected_1,"object_detected_2=", object_tools.object_detected_2)
    print("butt_len1=", butt_len1, "butt_len2=", butt_len2, "butt_len3=", butt_len3, "butt_len4=", butt_len4)        
     
   
    #Test for Object Detected and do lights
    if object_tools.object_detected:
        brick.light.on(Color.ORANGE)
    else:
        brick.light.on(Color.GREEN)

    # Do IR buttons
    # Check for button press on Chan 1
    chan = 1
    buttons = ir.buttons(chan)
    butt_len1=len(buttons)
      
    # Exit Button
    if ( Button.BEACON in buttons ):
     main_loop =False
     
    # Check for button press on Chan 2 and execute Move commands
    chan = 2  
    buttons = ir.buttons(chan)   
    butt_len2= len(buttons)

    # Exit Button
    if (Button.BEACON in buttons):
        main_loop =False
    
    # Check for button press on Chan 3 and execute Move commands
    chan = 3
    buttons = ir.buttons(chan)
    butt_len3 =len(buttons)
 
    # Exit Button
    if Button.BEACON in buttons  :
        main_loop =False

    # Check for button press on Chan 4 and execute Move commands
    chan = 4
    buttons = ir.buttons(chan)
    butt_len4 =len(buttons)
 
    # Use Beacon on Chan 4 to play directions sounds
    if Button.BEACON in buttons  :
        if direction > 10:
            direction =0
        motion_tools.direction_sound(direction,True)
        direction = direction +1

    #start motor logging

    if Button.LEFT_UP in buttons:
        time_seconds = 10
        fileA ="logA.txt"
        fileD ="logD.txt"
        sound_tools.play_file(SoundFile.START)
        motion_tools.start_log_motorA(time_seconds)
        motion_tools.start_log_motorD(time_seconds)
        wait(1.5*1000*time_seconds)
        motion_tools.save_log_motorA(fileA)
        motion_tools.save_log_motorD(fileD)
        sound_tools.play_file(SoundFile.STOP)

    

    wait(10)
    

# Terminate progam  after saying stop
object_tools.object_detect_loop = False
motion_tools.scan_head_loop =False
sound_tools.play_file(SoundFile.STOP)
