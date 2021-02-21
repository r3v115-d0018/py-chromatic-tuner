import aubio
import math
import sys

name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def findnote(freq, C0):
    h = round(12*math.log(freq/C0,2))
    octave = int(h // 12)
    n =int(h % 12)
    return (name[n], octave)

def colorize(string, errorper, tolerance):
    if errorper <= tolerance:
	return '\033[32m' + string + '\033[0m'
    elif errorper < 0.33:
	return '\033[93m' + string + '\033[0m'
    elif errorper < 0.66:
        return '\033[33m' + string + '\033[0m'
    else:
        return '\033[91m' + string + '\033[0m'

# def initStream():
#     #PyAudio stream object.
#     p = pyaudio.PyAudio()
    
#     #Open the stream.
#     stream = p.open(format=pyaudio.paFloat32,
#      		    channels=1,rate=44100,input=True,
#                     frames_per_buffer=1024)
    
#     return stream


def initStream():
    if len(sys.argv) < 2:
        print("Provide a wave file.\nOthers like MP3 also should work, but not necessarily.\n\nUsage: python %s filename.wav" % sys.argv[0])
        sys.exit(-1)

    # wf = wave.open(sys.argv[1], 'rb')
    # stream = librosa.stream(sys.argv[1], block_length=1, frame_length=1024, hop_length=1)
    stream = aubio.source(sys.argv[1], 44100, 512)

    # return wf
    return stream


def initDetector():
    # Aubio's pitch detection.
    # If detection with current algorithm
    # gives some false positives then
    # change to: yinfast or yin or maybe the other one
    # while detecting a pitch there is a need to check
    # whether a pitch is equal to 0 "zero"
    # because it is not either frequency in tune with actual A4
    # or not, it is simply a silence so probably
    # should be excluded from results/counting
    pDetector = aubio.pitch("default", 4096, 512, 44100)
    # Set unit.
    pDetector.set_unit("Hz")
    pDetector.set_silence(-20)
    # pDetector.set_tolerance(0.8)

    return pDetector
