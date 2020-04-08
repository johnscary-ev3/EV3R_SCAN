#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick 
brick = EV3Brick()

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from threading import Thread

import sound_tools
import object_tools

#Variables
scan_head_loop = True
scan_head_move = False
scan_head_move_2 = False

#init Head motors
def Init_MotorA():
    global motorA
    motorA = Motor(Port.A)

def Init_MotorD():
    global motorD
    motorD = Motor(Port.D)

#Init Scan Head
#Home at +90 or -90dg
def init_scan_head(head_speed,homedirection,homeoffset):
    if(homedirection):
        motorA.run_until_stalled(head_speed, Stop.BRAKE, 50)
        motorA.reset_angle(0)
        motorA.run_target(head_speed, homeoffset, Stop.BRAKE, True)
    else:
        motorA.run_until_stalled(-head_speed, Stop.BRAKE, 50)
        motorA.reset_angle(0)
        motorA.run_target(head_speed, homeoffset, Stop.BRAKE, True)

    motorA.reset_angle(0)

#Init Scan Head 2
#Home at +90 or -90dg
def init_scan_head_2(head_speed,homedirection,homeoffset):
    if(homedirection):
        motorD.run_until_stalled(head_speed, Stop.BRAKE, 50)
        motorD.reset_angle(0)
        motorD.run_target(head_speed, homeoffset, Stop.BRAKE, True)
    else:
        motorD.run_until_stalled(-head_speed, Stop.BRAKE, 50)
        motorD.reset_angle(0)
        motorD.run_target(head_speed, homeoffset, Stop.BRAKE, True)

    motorD.reset_angle(0)
    


# Move Scan Head with Target Angle
def move_scan_head_target(head_speed, target_angle, wait = True):
    motorA.run_target(head_speed, target_angle, Stop.COAST, wait)

#Move Scan Head with Target Angle
def move_scan_head_target_2(head_speed, target_angle, wait = True):
    motorD.run_target(head_speed, target_angle, Stop.COAST, wait)

# Home Scan Head to zero dg
def home_scan_head():
    global scan_head_speed
    move_scan_head_target(scan_head_speed, 0)

# Home Scan Head 2 to zero dg
def home_scan_head_2():
    global scan_head_speed
    move_scan_head_target_2(scan_head_speed, 0)


def direction_sound(direction,GoSound = True):
    # This function  says Direction Number
    if GoSound:
        sound_tools.play_file(SoundFile.GO)
    if direction == 0:
        sound_tools.play_file(SoundFile.ZERO)
    elif direction == 1:
        sound_tools.play_file(SoundFile.ONE)
    elif direction == 2:
        sound_tools.play_file(SoundFile.TWO)
    elif direction == 3:
        sound_tools.play_file(SoundFile.THREE)  
    elif direction == 4:
        sound_tools.play_file(SoundFile.FOUR)    
    elif direction == 5:
        sound_tools.play_file(SoundFile.FIVE)    
    elif direction == 6:
        sound_tools.play_file(SoundFile.SIX)    
    elif direction == 7:
        sound_tools.play_file(SoundFile.SEVEN)  
    elif direction == 8:
        sound_tools.play_file(SoundFile.EIGHT)
    elif direction == 9:
        sound_tools.play_file(SoundFile.NINE) 
    elif direction == 10:
        sound_tools.play_file(SoundFile.TEN)               


#Set up scan head thread
def scan_head_thread():
    global scan_head_loop
    global scan_head_move
    global scan_head_move_2
    global scan_head_speed
    scan_head_wait =1000
    while scan_head_loop:
        #Double check scan_head_loop since it could change while we are in the scan loop
        # set up the move wait options
        if scan_head_move_2:
            move_wait_1 = False
        else:
            move_wait_1 = True
        move_wait_2 = True

        #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed,-25, move_wait_1)
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed,-25, move_wait_2)
        if scan_head_loop:
            object_tools.sonic_sensor_lock.release()
            wait(scan_head_wait)

        #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed,-50, move_wait_1)
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed,-50, move_wait_2)
        if scan_head_loop:    
            object_tools.sonic_sensor_lock.release()
            wait(scan_head_wait)

        #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed,-25, move_wait_1)
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed,-25, move_wait_2)
        if scan_head_loop:
            object_tools.sonic_sensor_lock.release()
            wait(scan_head_wait)

        #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed,  0, move_wait_1)
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed,  0, move_wait_2)
        if scan_head_loop:
            object_tools.sonic_sensor_lock.release()
            wait(scan_head_wait)

         #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed, 25, move_wait_1)
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed, 25, move_wait_2)
        if scan_head_loop:
            object_tools.sonic_sensor_lock.release()
            wait(scan_head_wait)

        #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed, 50, move_wait_1)
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed, 50, move_wait_2)
        if scan_head_loop:
            object_tools.sonic_sensor_lock.release()
            wait(scan_head_wait)

        #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed, 25, move_wait_1)
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed, 25, move_wait_2)
        if scan_head_loop:
            object_tools.sonic_sensor_lock.release()
            wait(scan_head_wait)

        #Use Lock/Release of the Sonic sensor thread flag
        if scan_head_loop:
            object_tools.sonic_sensor_lock.acquire()
        if scan_head_move and scan_head_loop:
            move_scan_head_target(scan_head_speed,  0, move_wait_1)  
        if scan_head_move_2 and scan_head_loop:
            move_scan_head_target_2(scan_head_speed,  0, move_wait_2)
        if scan_head_loop:
            object_tools.sonic_sensor_lock.release()    
            wait(scan_head_wait)

#Start scan head thread
def start_scan_head_thread():
    t_scan_head_thread = Thread(target=scan_head_thread)
    t_scan_head_thread.start()




