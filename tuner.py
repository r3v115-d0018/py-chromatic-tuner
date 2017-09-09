from __future__ import print_function
import pyaudio, aubio, wave
import sys, time, getopt
import numpy as num
import math
import utility

A4 = 440
C0 = A4 * pow(2, -4.75)

octave0 = {}

temp = C0
for x in utility.name:
    octave0[x] = temp
    temp = temp * pow(2, 1.0/12) 

stream = utility.initStream()
pDetector = utility.initDetector()

while True:
    data = stream.read(1024)
    samples = num.fromstring(data, dtype=aubio.float_type)
    pitch = pDetector(samples)[0]
    
    if pitch!= 0: 
	note,octave = utility.findnote(pitch, C0)
    	output = "Pitch:" + str(pitch) + "Hz Note:" + note + str(octave) + "            "
        
        accuracy = 5

        expected = octave0[note] * pow(2, octave)
        error = pitch - expected
        
        tolerance = 0.1
        
        if error > 0:
            margin = expected * (pow(2,1.0/24) - 1)
        else:
            margin = expected * (1 - pow(2,-1.0/24))
        
        errorper = abs(error) / margin
        if  errorper > 1:
            print("Error greater than 100% at pitch : " + pitch)
            exit()
        if errorper <= tolerance:
            print (accuracy * "  ." + utility.colorize("  ^  ", errorper, tolerance) + accuracy * ".  " + output + '\r',end = '')
        else:
            if error > 0:
                pre = accuracy * "  ." + "  "
                pos = int(math.ceil(accuracy*errorper))
                post = (pos - 1) * "  ." + utility.colorize("  <", errorper, tolerance) + (accuracy - pos) * "  ."
            else:
                post = accuracy * "  ."
                pos = accuracy - int(math.ceil(accuracy*errorper)) + 1
                pre = "  " + (pos - 1) * ".  " + utility.colorize(">  ", errorper, tolerance) + (accuracy - pos) * ".  "
        
            print (pre + "|" + post + "  " + output + '\r', end = '')
	sys.stdout.flush()
