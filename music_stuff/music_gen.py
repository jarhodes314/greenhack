from audio import *
import time, random

class MusicGen:
    happy = True

    minorMapping = {
        0:"A",
        1:"B",
        2:"C",
        3:"D",
        4:"E",
        5:"F",
        6:"G"
    }
    majorMapping = {
        0:"A",
        1:"B",
        2:"C#",
        3:"D",
        4:"E",
        5:"F#",
        6:"G#"
    }

def playNote(note, octave):
    generator.addTune(Tune(notefade(Notes.freq(note, octave), 20), generator.elapsedTime, 20))

def playNext():
    nt = random.randint(0, 6)
    if(happy == True):
        playNote(nt, 0)
        

playNote("C", 1)


generator.start()
generator.wait(1, playNext)



