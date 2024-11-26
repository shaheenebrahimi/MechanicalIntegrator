#!/usr/bin/env python

import pigpio
from time import sleep, perf_counter
from math import *
import numpy as np
import tkinter as tk
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv

from stepper import Stepper
from encoder import Encoder

class MechanicalIntegrator:
    
    stepperGPIO = [6, 5] # GPIO ports for STEP and DIR of stepper motor
    encoderGPIO = [4, 17] # GPIO ports for A and B of encoder
    sampleRate = 100
    maxSteps = 9200 # corresponds to distance from center to edge of disk
   
    def setup(self):
        self.pi = pigpio.pi()
        self.stepper = Stepper(self.pi, self.stepperGPIO[0], self.stepperGPIO[1])
        self.encoder = Encoder(self.pi, self.encoderGPIO[0], self.encoderGPIO[1])

    def cleanup(self):
        self.encoder.endListen()
        self.stepper.resetPosition() # bring linear motion payload back to center
    
    def stop(self):
        self.pi.stop()
        
    def run(self):
        self.equation = self.inputBox.get()
        self.leftBound = self.inputLeftBound.get()
        self.rightBound = self.inputRightBound.get()
        self.logic(self.equation, self.leftBound, self.rightBound)
        
    def __init__(self):
        self.setup()
        self.GUI()
    
    def GUI(self): # create GUI to input equation and bounds
        self.frame = tk.Tk()
        self.frame.title("Mechanical Integrator")
        self.frame.geometry('310x110')
        self.frame.attributes('-topmost', True)
        self.frame.resizable(False,False)
        tk.Label(self.frame,text="y = ").grid(row=0,column=0)
        self.inputBox = tk.Entry(self.frame)
        self.inputBox.grid(row=0,column=1,sticky="nsew")
        tk.Label(self.frame,text="Left Bound: ").grid(row=1,column=0)
        self.inputLeftBound = tk.Entry(self.frame)
        self.inputLeftBound.grid(row=1,column=1,sticky="ew")
        tk.Label(self.frame,text="Right Bound: ").grid(row=2,column=0)
        self.inputRightBound = tk.Entry(self.frame)
        self.inputRightBound.grid(row=2,column=1,sticky="ew")
        self.submitButton = tk.Button(self.frame, text="GO", command=self.run).grid(row=3,column=0)
        self.outputLabel = tk.Label(self.frame, text = "")
        self.outputLabel.grid(row=3,column=1)
        self.frame.mainloop()
    
    def setOutput(self, result): # update GUI with steps of process
        self.outputLabel.config(text = str(result))
        self.frame.update()
        self.frame.focus()
        
    def getX(self, leftBound, rightBound): # creates set of bounded x vals to evaluate upon 
        xVals = np.linspace(leftBound, rightBound, num=self.sampleRate)
        return xVals
    
    def getY(self, equation, xVals): # creates set of y Vals from equation calculations
        yVals = []
        for x in xVals:
            try:
                y = equation.replace('x',"("+str(x)+")")
                yVals.append(eval(y))
            except Exception as e:
                print(e)
        return np.asarray(yVals)
        
    def createBoundingBox(self, xVals, yVals): # bounding box based upon absolute minima and maxima
        maxBound = abs(np.amin(yVals))
        minBound = abs(np.amax(yVals))
        yBound = maxBound if maxBound >= minBound else minBound
        stepSize = (yBound) / self.maxSteps
        return stepSize

    def stepSequence(self, yVals, stepSize): # convert y values into steps for stepper motor
        sequence = []
        speeds = []
        for i in range(1, len(yVals)):
            steps = int((yVals[i] - yVals[i-1]) / stepSize)
            sequence.append(steps)
        return np.asarray(sequence)
    
    def executeSteps(self, stepSequence): # execute a sequence of steps and record total timing
        y_vals = []
        y_vals.append(self.encoder.position())
        for steps in stepSequence:
            speed = self.stepper.calculateSpeed(abs(steps))
            start = perf_counter()
            self.stepper.step(steps, speed)
            y_vals.append(self.encoder.position())
        return np.asarray(y_vals)
    
    def plot(self, x_vals, y_vals, output_vals): # graph the function
        fig = make_subplots(rows=2,cols=1, subplot_titles=["Input Function", "Output Function"], vertical_spacing=0.075)
        fig.append_trace(go.Scatter(mode='lines', x=x_vals,y=y_vals, name="y(x)"), row=1, col=1)
        fig.append_trace(go.Scatter(mode='lines', x=x_vals, y=output_vals, name="Y(x)"), row=2, col=1)
        fig.update_yaxes(showticklabels=False)
        fig.show()

    def logic(self, equation, leftBound, rightBound): # main function
        xVals = self.getX(float(leftBound), float(rightBound))
        yVals = self.getY(equation, xVals)
        
        stepSize = self.createBoundingBox(xVals, yVals)
        stepSequence = self.stepSequence(yVals, stepSize)
        initialSteps = self.stepSequence([0,yVals[0]], stepSize)
        
        self.setOutput("Setting Initial Position")
        self.stepper.setInitialPosition(initialSteps)
          
        self.setOutput("Calculating ...")
        sleep(2)
        self.encoder.startListen()
        output_y = self.executeSteps(stepSequence)
        self.encoder.endListen()
        sleep(2)        
        
        self.setOutput("Resetting ...")
        self.cleanup()
        
        self.setOutput("Outputting Result")
        try:
            self.plot(xVals, yVals, output_y)
        except Exception as e:
            self.setOutput("No Output")
            print(e)
            return
        self.setOutput("Done")
            
mech = MechanicalIntegrator()