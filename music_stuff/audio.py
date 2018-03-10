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

def callback(in_data, frame_count, time_info, status):
    data = generator.volume * generator.generateDuration(frame_count / generator.fs, frame_count)

    if generator.exit:
        outputStatus = pyaudio.paAbort
    else:
        outputStatus = pyaudio.paContinue

    return (data, outputStatus)


class AudioGenerator:
    tunes = []
    tuneHeap = []
    elapsedTime = 0.0
    lastVolume = 1.0
    volume = 0.2
    fs = 44100
    stream = None
    exit = False

    def start(self):
        self.stream = p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=self.fs,
                             output=True,
                             stream_callback=callback,
                             frames_per_buffer=1024)

    def wait(self,period=0.1,cb=None):
        while self.stream.is_active():
            time.sleep(period)

            if cb is not None:
                cb(generator.elapsedTime)

        self.stream.stop_stream()
        self.stream.close()

        p.terminate()

    def addTune(self, tune):
        heapq.heappush(self.tuneHeap, tune)

    def generateDuration(self, duration, frames):

        # add to the tunes the ones that will start playing during this time
        while len(self.tuneHeap) > 0 and self.tuneHeap[0].start < self.elapsedTime + duration:
            self.tunes.append(heapq.heappop(self.tuneHeap))

        timesteps = self.elapsedTime + (np.arange(frames) * (1 / self.fs))
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

        samples *= (np.arange(0.0, 1.0, 1.0 / frames) * (1.0 / sumVolume) + (
                    1.0 - np.arange(0.0, 1.0, 1.0 / frames)) * (1.0 / self.lastVolume))

        self.lastVolume = sumVolume

        output = samples.astype(np.float32)

        self.elapsedTime += duration

        return output


p = pyaudio.PyAudio()


def note(freq):
    def notesound(t):
        return math.sin(2 * math.pi * freq * t)

    return np.vectorize(notesound)

def ins1(x):
    return 0.5 * (math.sin(x) + math.sin(2 * x) + math.cos(math.sin(3 * x)) - 0.225)

def ins2(x):
    return 0.5 * (math.sin(x) + (1/2) * math.sin(2 * x) + (1/3) * math.sin(3 * x))

def ins3(x):
    return math.sin(math.cos(x)) + math.cos(math.sin(x)) - 1

def ins4(x):
    return 0.25 * (math.sin(x) + math.cos(2 * x) + math.sin(3 * x) + math.cos(4 * x) + math.sin(5 * x) + math.cos(6 * x) - 0.5)

def notefade(freq, p):
    ran = random.randint(0,3)

    if ran == 0:
        ins = ins1
    elif ran == 1:
        ins = ins2
    elif ran == 2:
        ins = ins3
    else:
        ins = ins4

    def notesound(t):
        x = 2 * math.pi * freq * t

        return ins(x) * math.exp(-p * t)

    return np.vectorize(notesound)

class Notes:
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

    @staticmethod
    def numfreq(num):
        return pow(2, (num - 1) / 12) * 440

    @staticmethod
    def freq(key, octave=0):
        return pow(2, (Notes.nf[key] - 1 + 12 * octave) / 12) * 440


generator = AudioGenerator()

#changed this file so I can commit

