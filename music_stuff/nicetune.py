from music_stuff.audio import *
import random

generator.start()

noteA = 0
noteB = 0
direction = 0

counter = 0
nextRepeats = 3

def cb(start):
    global direction
    global noteA
    global noteB
    global counter
    global nextRepeats

    noteChoice = random.randint(0, 1)

    forward = 0.1
    length = 5
    # decay = 1.5 + random.randint(0,1)
    decay = 3.5

    if noteChoice == 0:
        freq = Notes.numfreq(noteA)
    else:
        freq = Notes.numfreq(noteB)

    volume = (5 - counter) * (1 / 5)

    if random.random() < 0.3:
        direction = 1 - direction

    if counter == nextRepeats:
        counter = 0
        nextRepeats = random.randint(0,5)
        if direction == 0:
            if noteChoice == 0:
                noteA += 1
            else:
                noteB += 1
        else:
            if noteChoice == 0:
                noteA -= 1
            else:
                noteB -= 1
    else:
        counter += 1

    generator.addTune(Tune(notefade(freq, decay, volume), start + forward, length))

generator.wait(0.333, cb)
