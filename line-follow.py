#!/usr/bin/python

# Created by Harry Merckel

import RPi.GPIO as GPIO
import time

# Setting up the GPIO pins for the motors and override switch
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT) # Motor 1 - forwards
GPIO.setup(19, GPIO.OUT) # Motor 1 - backwards
GPIO.setup(26, GPIO.OUT) # Motor 2 - forwards
GPIO.setup(24, GPIO.OUT) # Motor 2 - backwards
GPIO.setup(11, GPIO.IN) #
GPIO.setup(12, GPIO.IN) #
GPIO.setup(13, GPIO.IN) # 
GPIO.setup(7, GPIO.IN) # Override switch

# Setting up PWM for speed control and starting motors at 0 so no output.
m1f = GPIO.PWM(21, 50)
m1b = GPIO.PWM(19, 50)
m2f = GPIO.PWM(26, 50)
m2b = GPIO.PWM(24, 50)

m1f.start(0)
m1b.start(0)
m2f.start(0)
m2b.start(0)

# This function is to simplify the motor control instead of having to use the ChangeDutyCycle function throughout the program.
def motor (l, r):
    if l > 0:
        m1f.ChangeDutyCycle(l)
        m1b.ChangeDutyCycle(0)
    else:
        m1f.ChangeDutyCycle(0)
        m1b.ChangeDutyCycle(-l)
    if r > 0:
        m2f.ChangeDutyCycle(r)
        m2b.ChangeDutyCycle(0)
    else:
        m2f.ChangeDutyCycle(0)
        m2b.ChangeDutyCycle(-r)
        
def checkLine():
    # This checks the line following sensor and acts accordingly.
    l = GPIO.input(11)
    c = GPIO.input(12)
    r = GPIO.input(13)
    if not l and c and not r: return
    if l and c and not r:
        motor(100,100)
        return
    if l and not c and not r:
        motor(-50,100)
        return
    if not l and c and r:
        motor(100,0)
        return
    if not l and not c and r:
        motor(100,-50)
        return
    if not l and not c and not r:
        motor(100,100)
        return
    if l and c and r:
        motor(100,100)
        return
            
# Checks if a connection is not made on pin 7 (switch) as an emergency stop and restarts program.
def checkSwitch():
    active = not GPIO.input(7)
    if active:
        return
    else:
        motor(0, 0)
        start()
            
# The start function checks for the switch every two seconds if it's off.
def start():
    while True:
        print "start"
        active = not GPIO.input(7)
        if active:
            return
        else:
            time.sleep(2)
            
motor(0, 0)

start()

# This loops runs it all.
while True:
    checkSwitch()
    checkLine()
    time.sleep(0.1)

motor (0, 0)

GPIO.cleanup()
