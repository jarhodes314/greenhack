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

def cb(start):
    forward = random.random() * 2.0 + 1.0
    length = 5
    decay = random.random() + 1.0
    freq = Notes.numfreq(random.randint(-30, 30))

    generator.addTune(Tune(notefade(freq, decay), start + forward, length))

generator.wait(0.3, cb)
