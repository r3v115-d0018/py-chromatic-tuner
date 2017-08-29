from __future__ import print_function
import aubio
import numpy as num
import pyaudio
import math
import wave
import time
import sys

#print("Hi")
A4 = 440
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

octave0 = {}

temp = C0
for x in name:
    octave0[x] = temp
    temp = temp * pow(2, 1.0/12) 



def findnote(freq):
    h = round(12*math.log(freq/C0,2))
    octave = int(h // 12)
    n =int(h % 12)
    return (name[n], octave)

def colorize(string, position):
    if position == 3:
        return '\033[31m' + string + '\033[0m'
    elif position == 2:
        return '\033[33m' + string + '\033[0m'
    elif position == 1:
        return '\033[93m' + string + '\033[0m'
    else:
        return '\033[32m' + string + '\033[0m'

#PyAudio stream object.
p = pyaudio.PyAudio()

#Open the stream.

stream = p.open(format=pyaudio.paFloat32,
		channels=1,rate=44100,input=True,
		frames_per_buffer=1024)

# Aubio's pitch detection.
pDetection = aubio.pitch("default", 2048,
    2048//2, 44100)
# Set unit.
pDetection.set_unit("Hz")
pDetection.set_silence(-10)

prevpitch = 0

while True:
    data = stream.read(1024)
    samples = num.fromstring(data,
        dtype=aubio.float_type)
    pitch = pDetection(samples)[0]

    # Compute the energy (volume) of the
    # current frame.
    # Format the volume output so that at most
    # it has six decimal numbers.

    #pitch = 427.76

    if pitch!= 0 and abs(prevpitch - pitch) > 1.5 :
        #prevpitch = 0
        prevpitch = pitch
	note,octave = findnote(pitch)
    	output = "Pitch:" + str(pitch) + "Hz Note:" + note + str(octave) + "            "
        

        expected = octave0[note] * pow(2, octave)
        error = pitch - expected
        
        tolerance = 0.1
        
        if error > 0:
            margin = 0.5 * (pitch * pow(2, 1.0 / 12) - pitch)
        else:
            margin = 0.5 * (pitch - pitch * pow(2,-1.0/12))
        
        errorper = abs(error) / margin
        
        if errorper <= tolerance:
            print ("  .  .  ." + colorize("  ^  ", 0) + ".  .  .  " + output + '\r',end = '')
        else:
            if error > 0:
                pre = "  .  .  .  "
                pos = int(math.ceil(3*errorper))
                post = (pos - 1) * "  ." + colorize("  <", pos) + (3 - pos) * "  ."
            else:
                post = "  .  .  ."
                pos = 3 - int(math.ceil(3*errorper)) + 1
                pre = "  " + (pos - 1) * ".  " + colorize(">  ", 4 - pos) + (3 - pos) * ".  "
        
            print (pre + "|" + post + "  " + output + '\r', end = '')
	sys.stdout.flush()
