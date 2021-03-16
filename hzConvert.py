#! python

# Script to convert scientific pitch notation to Hz
# Brad Gersh
# Started: 2017-01-11
# Last revised: 2017-05-09
# Updated 2019-01-07 to add MIDI to Pitch Name module.
# Updated 2020-03-20 to add capability for pitch sets in pitchToHz module.
# Updated 2020-08-01 for Python 3 compatibility.

import math

A4Hz = 440.0 

def pitchToHz():
    pass

def pitchToHzTool():
    print("A4 = %.3f Hz" % A4Hz)
    print("\nEnter a list of pitches in scientific pitch notation (separated by spaces) press ENTER. Format is pitch name (A-G), accidental (see next), and octave (an integer), all without spaces. Examples: Cn4, Bb8, F#4.\n\nAccidentals can be #, b, or n (natural). Double sharps and flats are indicated by x and d (a single-character version of double flat). Rational accidentals are indicated by a fraction before the accidental in parens, e.g. (1/4)#, (2/3)b. Accidentals MAY NOT BE OMITTED. e.g. B(3/4)#8.\n\nWARNING: Quarter tones are indicated by HALF accidentals. This is because accidentals themselves already embed semitones. Thus a quarter tone above Cn4 is C \'half sharp\', or C(1/2)#4.\n\nExample input: Cn4 D#6 B(1/2)b3")

    print("\nType X to quit.")

    noteNames = set(["A", "B", "C", "D", "E", "F", "G"])
    accids = set(["n", "d", "b", "#", "x"])

    debug = False
    debugSwitch = input("Type D here for debug messages:")
    if debugSwitch in ("D", "d"):
        debug = True

    while True:
        err = False
        partOfPitch = 1
        noteName = ""
        accid = ""
        rationalFlag = False
        rationalUsed = False
        rationalEverUsed = False
        numeratorFlag = False
        denominatorFlag = False
        negOctave = False
        numerator = 0
        denominator = 1
        ratio = 0.0
        octave = 0
        pitch = input("\nPitches: ")

        # Parse inputted note
        if pitch in ("X", "x"):
            break
        currPitch = 0
        midiNote = []
        distance = []
        Hz = []
        if debug: print("Parsing character by character ...")
        for c in pitch:
            if debug: print("char = %s, currPitch = %i, partOfPitch = %i" % (c, currPitch, partOfPitch))

            if c == "":
                break
            if c == " ":
                if debug: print("Advancing to next note.")
                currPitch += 1
                partOfPitch = 0

            if partOfPitch == 3:
                if c=="-":
                    negOctave = True
                else:
                    try:
                        octave = int(("%i" + c) % octave)
                        if debug: print("Octave assigned")
                    except ValueError:
                        print("Invalid format err 1")
                        err = True
                        break

                if err==True:
                    if debug: print("Something just went wrong.")
                if err==False:
                    ratio = float(numerator) / denominator
                    if negOctave:
                        octave = octave * (-1)
                    if debug: print("--- Note name: " + noteName + " Accid: " + accid + " Accid Ratio: %.3f Octave: %i" % (ratio, octave))
            
                    # Convert inputted note to MIDI note (possibly a rational number)
                    # C-1 = 0, C4 = 60, A4 = 69
                    diatonicClass = 0
                    pitchClass = 0
                    accidValue = 0.0
                    if noteName == "C": diatonicClass = 0
                    if noteName == "D": diatonicClass = 2
                    if noteName == "E": diatonicClass = 4
                    if noteName == "F": diatonicClass = 5
                    if noteName == "G": diatonicClass = 7
                    if noteName == "A": diatonicClass = 9
                    if noteName == "B": diatonicClass = 11
                    if accid == "d": accidValue = -2
                    if accid == "b": accidValue = -1
                    if accid == "n": accidValue = 0
                    if accid == "#": accidValue = 1
                    if accid == "x": accidValue = 2
                    if rationalUsed:
                        accidValue = accidValue * ratio

                    midiNote.append((diatonicClass + 12*(octave+1)) + accidValue)
                    # Convert MIDI note to Hz
                    # A4 = 69. Count semitones from A4.
                    midiRef = 69 # The MIDI value for A4
                    distance.append(midiNote[currPitch] - midiRef)
                    stHz = 2**(1.0/12)
                    Hz.append(A4Hz * (stHz**(distance[currPitch])))

            if partOfPitch == 2:
                if debug: print("Detecting accidental ...")
                accidSuccess = False
                if c == ")":
                    rationalFlag = False
                    if debug: print("Rational flag off")
                    accidSuccess = True
                if rationalFlag == False and c in accids:
                    if rationalUsed == False:
                        accid = c
                        if debug: print("Accidental assigned")
                        partOfPitch += 1
                        accidSuccess = True
                    if rationalUsed == True:
                        if c in set(["n", "d", "x"]):
                            print("Error: Only b and # accidentals are valid with rational accidentals.")
                            err = True
                            break
                        else:
                            accid = c
                            if debug: print("Accidental assigned")
                            partOfPitch += 1
                            accidSuccess = True
                if rationalFlag:
                    if denominatorFlag:
                        try:
                            denominator = int(c)
                            if debug: print("Denominator assigned")
                            denominatorFlag = False
                            accidSuccess = True
                        except ValueError:
                            print("Invalid format err 2")
                            err = True
                            break
                    if c == "/":
                        numeratorFlag = False
                        denominatorFlag = True
                        accidSuccess = True
                    if numeratorFlag:
                        try:
                            numerator = int(c)
                            if debug: print("Numerator assigned")
                            accidSuccess = True
                        except ValueError:
                            print("Invalid format err 3")
                            err = True
                            break
                if c == "(":
                    rationalFlag = True
                    rationalUsed = True
                    numeratorFlag = True
                    if debug: print("Rational flag on.")
                    accidSuccess = True
                if accidSuccess == False:
                    print("Invalid format err 4")
                    err = True
                    break

            if partOfPitch == 1:
                if c in noteNames:
                    noteName = c
                    if debug: print("Note name assigned.")
                    partOfPitch += 1
                else:
                    print("Invalid format err 5")
                    err = True
                    break

            if partOfPitch == 0:
                if rationalUsed:
                    rationalEverUsed = True
                err = False
                partOfPitch = 1
                noteName = ""
                accid = ""
                rationalFlag = False
                rationalUsed = False
                numeratorFlag = False
                denominatorFlag = False
                negOctave = False
                numerator = 0
                denominator = 1
                ratio = 0.0
                octave = 0


        if rationalEverUsed:
            print("MIDI values: " + " ".join("%.2f" % n for n in midiNote)) # This syntax lifted from https://stackoverflow.com/questions/1566936/easy-pretty-printing-of-floats-in-python
            if debug: print("Semitone distances: " + " ".join("%.2f" % n for n in distance))
        else:
            print("MIDI values: " + " ".join("%i" % n for n in midiNote))
            if debug: print("Semitone distances: " + " ".join("%i" % n for n in distance))
        print("Hz values: " + " ".join("%.2f" % n for n in Hz))
    topmenu()

def HzToPitchTool():
    print("A4 = 440 assumed. Enter number as a decimal. Type X to quit.")

    while(True):
        pitch = ""
        midiNote = 0
        pitchClassNumber = 0
        pitchClassName = ""
        cents = 0.0
        octave = 0
        Hz = input("\nHz: ")

        if Hz in ("X", "x"):
            break

        try:
            # Ideally, fix bug where cents can be 100, e.g. C#4 + 100 c (which should read Dn4 + 0.0 c).
            Hz = float(Hz)
            midiNote = 12 * (math.log(Hz/440.0,2)) + 69
            print("MIDI value: %.3f" % midiNote)
            pitchClass = math.floor(midiNote) % 12
            if pitchClass == 0:
                pitchClassName = "Cn"
            elif pitchClass == 1:
                pitchClassName = "C#"
            elif pitchClass == 2:
                pitchClassName = "Dn"
            elif pitchClass == 3:
                pitchClassName = "Eb"
            elif pitchClass == 4:
                pitchClassName = "En"
            elif pitchClass == 5:
                pitchClassName = "Fn"
            elif pitchClass == 6:
                pitchClassName = "F#"
            elif pitchClass == 7:
                pitchClassName = "Gn"
            elif pitchClass == 8:
                pitchClassName = "Ab"
            elif pitchClass == 9:
                pitchClassName = "An"
            elif pitchClass == 10:
                pitchClassName = "Bb"
            elif pitchClass == 11:
                pitchClassName = "Bn"
            cents = 100 * (midiNote - math.floor(midiNote))
            octave = math.floor(midiNote/12.0) - 1
            print("Pitch name: " + pitchClassName + "%i + %.1f c" % (octave, cents))

        except ValueError:
            print("Not a decimal number.")
    topmenu()

        
def midiToPitchTool():
    print("A4 = 440 assumed. Enter number as a decimal. Type X to quit.")

    while(True):
        midiNote = input("\nMIDI: ")

        if midiNote in ("X", "x"):
            break

        try:
            # Ideally, fix bug where cents can be 100, e.g. C#4 + 100 c (which should read Dn4 + 0.0 c).
            midiNote = float(midiNote)
            pitchClass = math.floor(midiNote) % 12
            if pitchClass == 0:
                pitchClassName = "Cn"
            elif pitchClass == 1:
                pitchClassName = "C#"
            elif pitchClass == 2:
                pitchClassName = "Dn"
            elif pitchClass == 3:
                pitchClassName = "Eb"
            elif pitchClass == 4:
                pitchClassName = "En"
            elif pitchClass == 5:
                pitchClassName = "Fn"
            elif pitchClass == 6:
                pitchClassName = "F#"
            elif pitchClass == 7:
                pitchClassName = "Gn"
            elif pitchClass == 8:
                pitchClassName = "Ab"
            elif pitchClass == 9:
                pitchClassName = "An"
            elif pitchClass == 10:
                pitchClassName = "Bb"
            elif pitchClass == 11:
                pitchClassName = "Bn"
            cents = 100 * (midiNote - math.floor(midiNote))
            octave = math.floor(midiNote/12.0) - 1
            print("Pitch name: " + pitchClassName + "%i + %.1f c" % (octave, cents))

            # Convert MIDI note to Hz
            # A4 = 69. Count semitones from A4.
            midiRef = 69 # The MIDI value for A4
            distance = midiNote - midiRef
            stHz = 2**(1.0/12)
            Hz = A4Hz * (stHz**(distance))
            print("Hz value: %.3f" % Hz)


        except ValueError:
            print("Not a decimal number.")

    topmenu()

def topmenu():
    print("\nMake a selection:\n(1) Pitch name to Hz (and MIDI).\n(2) Hz to pitch name.\n(3) MIDI to pitch name.\n(X) Exit.")
    choice = input("> ")
    if choice == "1":
        pitchToHzTool()
    elif choice == "2":
        HzToPitchTool()
    elif choice == "3":
        midiToPitchTool()
    else:
        pass


def main():
    print("=== PITCH CONVERTER ===")
    print("Converts between different notations for pitch: Hz, MIDI, and pitch name.\n")
    A4Hz = input("Value for A4 in Hz (Press ENTER for default, A4=440)")
    if A4Hz == "":
        A4Hz = 440.0
    try:
        A4Hz = float(A4Hz)
    except ValueError:
        print("Press ENTER or input a number.")

    stHz = 2**(1.0/12)
    print("Semitone Hz = {}".format(stHz))

    topmenu()

    
if __name__ == "__main__":
    main()

