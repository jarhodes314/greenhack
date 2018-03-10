from music_stuff.audio import *
import random

# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
#
# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
# generator.addTune(Tune(notefade(442, 1.2), 0, 10))
# generator.addTune(Tune(notefade(442, 1.2), 0, 10))
# generator.addTune(Tune(notefade(440, 1.2), 0, 10))
# generator.addTune(Tune(notefade(560, 1.2), 3, 10))

generator.addTune(Tune(notefade(Notes.freq("C"), 2), 0, 2))
generator.addTune(Tune(notefade(Notes.freq("C"), 2), 0.3, 2))
generator.addTune(Tune(notefade(Notes.freq("C"), 2), 0.6, 2))

generator.addTune(Tune(notefade(Notes.freq("A"), 2), 1.2, 2))
generator.addTune(Tune(notefade(Notes.freq("C"), 2), 1.8, 2))
generator.addTune(Tune(notefade(Notes.freq("F"), 2), 2.4, 2))

generator.addTune(Tune(notefade(Notes.freq("F", -1), 2), 3.0, 1.2))

generator.start()

note = 0
direction = 0

def cb(start):
    global direction
    global note

    forward = 0
    length = 5
    decay = 1.5 + random.randint(0,1)
    freq = Notes.numfreq(note)

    if random.random() < 0.3:
        direction = 1 - direction

    if direction == 0:
        note += 1
    else:
        note -= 1


    generator.addTune(Tune(notefade(freq, decay), start + forward, length))

generator.wait(0.5, cb)
