#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick 
brick = EV3Brick()


from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
#from threading import Thread
from threading import (Thread, _thread)


import motion_tools
import sound_tools

# create a global lock object for sonic sensor reads
sonic_sensor_lock =  _thread.allocate_lock()

#Configuration Variables
UltrasonicSensorPort =Port.S2
UltrasonicSensorPort_2 =Port.S3
dist = 500
dist_2= 500
object_detect_limit = 300
object_detect_loop = True
object_detect_run = True
object_detect_run_2 = False
object_detected = False
object_detected_1 = False
object_detected_2 = False
object_detect_sound_on = False
object_detect_MoveMotorA_run = False

def Init_UltrasonicSensor():
    global us
    us = UltrasonicSensor(UltrasonicSensorPort)

def Init_UltrasonicSensor_2():
    global us_2
    us_2 = UltrasonicSensor(UltrasonicSensorPort_2)

#Object sound thread    
def object_sound_thread():
    global object_detected
    global object_detected_1
    global object_detected_2
    global object_detect_loop
    global object_detect_run
    global object_detect_sound_on
    while object_detect_loop:
        if  object_detected and object_detect_run and object_detect_sound_on:
            if object_detected_1 and not object_detected_2:
                sound_tools.play_file(SoundFile.DETECTED)
                sound_tools.play_file(SoundFile.ONE)
            elif not object_detected_1 and object_detected_2:
                sound_tools.play_file(SoundFile.DETECTED)
                sound_tools.play_file(SoundFile.TWO)
            elif object_detected_1 and object_detected_2:
                sound_tools.play_file(SoundFile.DETECTED)
                sound_tools.play_file(SoundFile.ONE)
                sound_tools.play_file(SoundFile.TWO)
        wait(100) 

#Start object sound thread
def start_object_sound_thread():
    t_object_sound_thread = Thread(target=object_sound_thread)
    t_object_sound_thread.start()


#get distance to objects
def get_object_dist():
    global us
    object_dist = us.distance(False)
    return object_dist

#get distance to objects Sensor 2
def get_object_dist_2():
    global us_2
    object_dist_2 = us_2.distance(False)
    return object_dist_2

#Set up object detect thread;  Handles 2 Sensors
def object_detect():
    global dist
    global dist_2
    global object_detected
    global object_detected_1
    global object_detected_2
    global object_detect_loop
    global object_detect_run
    global object_detect_run_2
    global object_detect_limit
    global sonic_sensor_lock
    while object_detect_loop:
        #Lock the Sonic sensor thread flag
        sonic_sensor_lock.acquire()

        #Sensor 1
        if object_detect_run:
            dist = get_object_dist()
            if dist < object_detect_limit:
                object_detected_1 =True  
            else:
                object_detected_1 =False
        else:
            object_detected_1 =False 

        #UN-Lock the Sonic sensor thread flag
        sonic_sensor_lock.release()

        if object_detected_1:
            object_detected = True

        #Wait some
        wait(100)

        #Lock the Sonic sensor thread flag again
        sonic_sensor_lock.acquire()

        #Sensor 2
        if object_detect_run_2:
            dist_2 = get_object_dist_2()
            if dist_2 < object_detect_limit:
                object_detected_2 = True  
            else:
                object_detected_2 = False
        else:
            object_detected_2 = False

        #UN-Lock the Sonic sensor thread flag
        sonic_sensor_lock.release()  

        #Set Combined Objected detected flag
        if object_detected_1 or object_detected_2:
            object_detected = True
        else:
            object_detected = False

        wait(100)

#Start object detect thread
def start_object_detect():
    t_object_detect = Thread(target=object_detect)
    t_object_detect.start()

