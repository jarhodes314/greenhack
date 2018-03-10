from music_stuff.audio import *
import random

generator.start()

generatedUpTo = 2

majors = [
    (7, ["C", "D", "E_", "F", "G", "A_", "B_"]),
    (3, ["E", "F#", "G", "A", "B", "C", "D"])
]

chords = [
    [1, 3, 5],
    [1, 4, 5],
    [1, 5, 6]
]

def addNote(scale, pos, start, duration, octave=0, p=2.0, volume=1.0):
    while pos < 0:
        pos += 6
        octave -= 1

    while pos > 6:
        pos -= 6
        octave += 1

    noteName = scale[1][pos]

    if scale[0] >= pos:
        octave += 1

    generator.addTune(Tune(notefade(Notes.freq(noteName, octave), p, volume), start, duration))


def cb(time):
    global generatedUpTo

    if time + 20 > generatedUpTo:
        start = generatedUpTo

        chord = chords[random.randint(0, len(chords) - 1)]
        scale = majors[random.randint(0, len(majors) - 1)]

        print(scale[1])

        addNote(scale, chord[0], start, 10, octave=-1, p=0.3)
        addNote(scale, chord[1], start, 10, octave=-1, p=0.3)
        addNote(scale, chord[2], start, 10, octave=-1, p=0.3)

        first = random.randint(0,2)
        last = random.randint(0,2)

        addNote(scale, first, start, 5, 1, 1.3, 2.0)
        addNote(scale, last, start + 2, 5, 1, 1.3, 2.0)

        if last == first:
            mid = first + random.randint(0,2)
            addNote(scale, mid, start + 1, 5, 1, 1.3, 2.0)

        else:
            mid = math.floor((first + last) / 2.0) + random.randint(-1,1)
            addNote(scale, mid, start + 1, 5, 1, 1.3, 2.0)


        generatedUpTo += 3


generator.wait(1.0, cb)
