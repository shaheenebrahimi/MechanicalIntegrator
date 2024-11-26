#!/usr/bin/env python

import pigpio 
    
class Encoder:
    
    """Class to decode mechanical rotary encoder pulses."""
    
    stepRatio = 1
    shaftRadius = 1.28
    rotationHistory = []
    
    def __init__(self, pi, gpioA, gpioB):
        self.pi = pi
        self.gpioA = gpioA
        self.gpioB = gpioB
        self.pos = 0

        self.levA = 0
        self.levB = 0

        self.lastGpio = None

        self.pi.set_mode(gpioA, pigpio.INPUT)
        self.pi.set_mode(gpioB, pigpio.INPUT)

        self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)
        
    def pulse(self, gpio, level, tick): # send pulse
        if gpio == self.gpioA: # if change in A
            self.levA = level # set level
        else:
            self.levB = level;

        if gpio != self.lastGpio: # debounce
            self.lastGpio = gpio

        if gpio == self.gpioA and level == 1: # clockwise
            if self.levB == 1:
                self.updatePos(1*self.stepRatio)
        elif gpio == self.gpioB and level == 1: # counter-clockwise
            if self.levA == 1:
                self.updatePos(-1*self.stepRatio)
                
    def startListen(self):
        self.cbA = self.pi.callback(self.gpioA, pigpio.EITHER_EDGE, self.pulse)
        self.cbB = self.pi.callback(self.gpioB, pigpio.EITHER_EDGE, self.pulse)

    def endListen(self): # cancel the callback functions
        self.cbA.cancel()
        self.cbB.cancel()
        self.reset()
    
    def updatePos(self, deltaPos): # update position of encoder
        self.pos += deltaPos
        self.rotationHistory.append(self.pos)
        
    def position(self): # return position of encoder
        return self.pos
    
    def reset(self):
        self.pos = 0
