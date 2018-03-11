import serial
import json
import requests
from audio import *
import time, random, _thread


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

def playNoteLong(note, octave):
    generator.addTune(Tune(notefade(Notes.freq(note, octave), 2, volume=0.5), generator.elapsedTime, 2))

def playNoteShort(note, octave):
    generator.addTune(Tune(notefade(Notes.freq(note, octave), 10, volume=1.0), generator.elapsedTime, 2))

nt = 3
def playNext(eltime):
    global nt
    nt = nt + random.randint(-1, 1)
    if nt < 0 or nt >= 7:
        nt = random.randint(0, 6)
    if(MusicGen.happy == True):
        #print("H")
        generator.period = 1
        playNoteLong("A", 0)
        playNoteLong(MusicGen.majorMapping[nt], 0)
    else:
        generator.period = 0.25
        #print("S")
        playNoteShort("A", 0)
        playNoteShort(MusicGen.minorMapping[nt], 0)

    
def ser_read():
    port = '/dev/ttyACM0'
    URL = 'https://greenhack.pythonanywhere.com/send_data'

    #f = open("JSONlog.txt", "a")

    ser = serial.Serial(port)
    with serial.Serial(port,9600,timeout = 1) as ser:
        global MusicGen
        while True:
            ln = str(ser.readline(), "UTF-8")
            #print(ser.readline())
            if ln != '':
                print(ln)
                #f.write(ln)
                data = json.loads(ln)
                r = requests.post(URL, data=data)
                if(data["potentiometer"]>800 or data["temperature"]>26):
                    ser.write(bytes("1", "UTF-8"))
                    MusicGen.happy = False
                else:
                    MusicGen.happy = True

    #f.close()


_thread.start_new_thread(ser_read, ())
generator.start()

generator.wait(1, playNext)




