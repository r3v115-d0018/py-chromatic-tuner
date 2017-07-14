import aubio
import numpy as num
import pyaudio
import math
import wave
import time

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
    return name[n] + str(octave)



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
    volume = num.sum(samples**2)/len(samples)
    # Format the volume output so that at most
    # it has six decimal numbers.
    volume = "{:.6f}".format(volume)


    if pitch!= 0 and abs(prevpitch - pitch) > 1.5 :
        prevpitch = pitch
	note = findnote(pitch)
    	output = "Pitch:" + str(pitch) + "Hz Note:" + note +   " Volume: " + str(volume) + "            "
        print output

        #FIX FOR #
	octave = int(note[1])
        expected = octave0[note[0]] * pow(2, octave)
        error = pitch - expected
        
        margin = 0.5 * (pitch + pitch * pow(2,1.0/12))
        tolerance = 0.1
        errorper = abs(error) / margin
        
        
	if errorper <= tolerance:
	    print "  .  .  .  ^  .  .  ."
        else:
             counter = 1
             spacing = 1.0/3
             temp = spacing
             while temp < 1:
                 if temp < errorper:
                     break;
                 counter = counter + 1
                 temp = temp + spacing
             if error > 0:
                 print "  .  .  .  |"
                 for i in range(3):
                     print "  "
                     if i == counter:
                         print "<"
                     else:
                         print "."
             elif error < 0:
                  counter = abs(counter - 4)
                  for i in range(3):
                      print "  "
                      if i == counter:
                          print ">"
                      else:
                          print "."
                  print "  |  .  .  ."    

