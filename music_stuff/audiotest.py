import math
import pyaudio
import numpy as np
import time
import heapq
import random

class Tune:

    def __init__(self, fun, start, duration):
        self.fun = fun
        self.start = start
        self.duration = duration

    def __lt__(self, other):
        return self.start < other.start

    def __eq__(self, other):
        return self.start == other.start

# a tune is a function, an elapsed time and a remaining length (before it is removed)

class AudioGenerator:

    tunes = []
    tuneHeap = []
    elapsedTime = 0.0
    lastVolume = 1.0

    # def __init__(self):
        # do init stuff

    def addTune(self, tune):
        heapq.heappush(self.tuneHeap, tune)

    def generateDuration(self, duration, frames):

        # add to the tunes the ones that will start playing during this time
        while len(self.tuneHeap) > 0 and self.tuneHeap[0].start < self.elapsedTime + duration:
            self.tunes.append(heapq.heappop(self.tuneHeap))

        timesteps = self.elapsedTime + (np.arange(frames) * (1 / fs))
        samples = np.zeros(frames)

        newTunes = []

        sumVolume = 0

        for tune in self.tunes:
            section = np.zeros(frames)
            section[np.logical_and(tune.start <= timesteps, timesteps < tune.start + tune.duration)] = 1.0

            changedTimes = (timesteps - tune.start) * section
            tuneSample = tune.fun(changedTimes) * section

            amp = np.amax(tuneSample)
            sumVolume += amp

            samples += tuneSample

            if tune.start + tune.duration > self.elapsedTime + duration:
                newTunes.append(tune)

        self.tunes = newTunes

        if sumVolume < 1.0:
            sumVolume = 1.0
        #print("ln 68: "+str(sumVolume))
        #print("ln 69: "+str(self.lastVolume))
        #print("ln 70: "+str(frames))
        samples *= (np.arange(0.0, 1.0, 1.0 / frames) * (1.0 / sumVolume) + (1.0 - np.arange(0.0, 1.0, 1.0 / frames)) * (1.0 / self.lastVolume))

        self.lastVolume = sumVolume

        output = samples.astype(np.float32)

        self.elapsedTime += duration

        return output


p = pyaudio.PyAudio()

volume = 0.2
fs = 44100
f = 440.0

def sound(t):
    n = math.sin(2*math.pi*math.pow(f*t, 1.0 + 0.5 * math.cos(math.pow(t, 0.9))))

    return n

def note(freq):
    def notesound(t):
        return math.sin(2*math.pi*freq*t)
    return np.vectorize(notesound)

def notefade(freq, p):
    def notesound(t):
        return math.sin(2*math.pi*freq*t) * math.exp(-p * t)
    return np.vectorize(notesound)


nf = {
    "A_": 0,
    "A": 1,
    "A#": 2,
    "B_": 2,
    "B": 3,
    "C": 4,
    "C#": 5,
    "D_": 5,
    "D": 6,
    "D#": 7,
    "E_": 7,
    "E": 8,
    "F": 9,
    "F#": 10,
    "G_": 10,
    "G": 11,
    "G#": 12
}

def fkey(key):
    return pow(2, (key - 1) / 12) * 440

vecsound = np.vectorize(sound)

generator = AudioGenerator()

# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
#
# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
# generator.addTune(Tune(notefade(442, 1.2), 0, 10))
# generator.addTune(Tune(notefade(442, 1.2), 0, 10))
# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
# generator.addTune(Tune(notefade(560, 1.2), 3, 10))

generator.addTune(Tune(notefade(fkey(nf["C"]), 20), 0, 2))
generator.addTune(Tune(notefade(fkey(nf["C"]), 20), 0.3, 2))
generator.addTune(Tune(notefade(fkey(nf["C"]), 20), 0.6, 2))

generator.addTune(Tune(notefade(fkey(nf["A"]), 20), 1.2, 2))
generator.addTune(Tune(notefade(fkey(nf["C"]), 20), 1.8, 2))
generator.addTune(Tune(notefade(fkey(nf["F"]), 20), 2.4, 2))

generator.addTune(Tune(notefade(fkey(nf["F"] - 12), 2), 3.0, 1.2))

def callback(in_data, frame_count, time_info, status):
    data = volume * generator.generateDuration(frame_count/fs, frame_count)
    return (data, pyaudio.paContinue)


stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True,
                stream_callback=callback)


while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()
