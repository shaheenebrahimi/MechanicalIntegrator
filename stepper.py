#!/usr/bin/env python

import pigpio
from time import sleep, perf_counter

class Stepper:
    
    """Class to control stepper motor speed and revolutions."""
    
    PHASE = 1.8 # specified angle per step
    SPR = 200   # Steps per Revolution: 200
    CW = 1      # clockwise
    CCW = 0     # counter clockwise

    def __init__(self, pi, gpioPUL, gpioDIR):
        self.pi = pi
        self.gpioPUL = gpioPUL
        self.gpioDIR = gpioDIR
        self.stepCount = 0
        
        self.pi.set_mode(self.gpioPUL, pigpio.OUTPUT)
        self.pi.set_mode(self.gpioDIR, pigpio.OUTPUT)
        
    def spin(self, revolutions=1, speed=1, direction=CW): # function for performing single stepper motor revolution
        self.pi.write(self.gpioDIR, direction)
        step_count = 8 * revolutions * int(self.SPR)
        delay = 1 / (self.SPR * speed)
        for x in range(step_count):
            self.pi.write(self.gpioPUL, 1)
            sleep(delay)
            self.pi.write(self.gpioPUL, 0)
            sleep(delay)
    
    def step(self, steps=1, speed=1): # function for performing 1/200th of a revolution (one step)
        direction = self.CW if steps <= 0 else self.CCW
        delta = steps
        steps = abs(steps)
        if (speed == 0):
            sleep(0.25)
            return
        self.pi.write(self.gpioDIR, direction)
        delay = 1 / (self.SPR * speed)
        for step in range(steps):
            self.pi.write(self.gpioPUL, 1)
            self.pi.write(self.gpioPUL, 0)
            sleep(abs(delay))
        self.stepCount += delta
        
    def setInitialPosition(self, initialSteps): # function used to calibrate around y-intercepts
        self.step(initialSteps[0], 500)

    def calculateSpeed(self, point): # using trend line from previous calibrations to determine ideal speeds
        return (0.00000000008 * point**4) + (0.00000001 * point**3) + (0.00001 * point**2) + (0.0227 * point)

    def resetPosition(self): # bring the linear motion payload back to center
        self.step(-self.stepCount,500)
        self.stepCount = 0
