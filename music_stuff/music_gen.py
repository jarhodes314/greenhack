from audio import *
import time, random, _thread

def moodch():
    while True:
        time.sleep(8)
        MusicGen.happy = False
        time.sleep(8)
        MusicGen.happy = True

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
    generator.addTune(Tune(notefade(Notes.freq(note, octave), 2), generator.elapsedTime, 2))

nt = 3
def playNext(eltime):
    playNote("A", 0)
    global nt
    nt = nt + random.randint(-1, 1)
    if nt < 0 or nt >= 7:
        nt = random.randint(0, 6)
    if(MusicGen.happy == True):
        print("H")
        playNote("C#", 0)
        playNote(MusicGen.majorMapping[nt], 0)
    else:
        print("S")
        playNote("C", 0)
        playNote(MusicGen.minorMapping[nt], 0)
    
        



_thread.start_new_thread(moodch, ())
generator.start()

generator.wait(1, playNext)






