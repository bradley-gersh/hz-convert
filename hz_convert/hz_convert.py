#! /usr/bin/env python3

"""
Script to convert scientific pitch notation to Hz
Brad Gersh
Started: 2017-01-11
Last revised: 2017-05-09
Recent revisions:
 - 2019-01-07: added MIDI to Pitch Name module.
 - 2020-03-20: added capability for pitch sets in pitch_to_hz_tool.
 - 2020-08-01: added Python 3 compatibility.
"""

import math

a4_hz = 440.0


def pitch_to_hz_tool():
    print("A4 = %.3f Hz" % a4_hz)
    print("\nEnter a list of pitches in scientific pitch notation (separated by spaces) press ENTER. Format is pitch name (A-G), accidental (see next), and octave (an integer), all without spaces. Examples: Cn4, Bb8, F#4.\n\nAccidentals can be #, b, or n (natural). Double sharps and flats are indicated by x and d (a single-character version of double flat). Rational accidentals are indicated by a fraction before the accidental in parens, e.g. (1/4)#, (2/3)b. Accidentals MAY NOT BE OMITTED. e.g. B(3/4)#8.\n\nWARNING: Quarter tones are indicated by HALF accidentals. This is because accidentals themselves already embed semitones. Thus a quarter tone above Cn4 is C \'half sharp\', or C(1/2)#4.\n\nExample input: Cn4 D#6 B(1/2)b3")

    print("\nType X to quit.")

    note_names = set(["A", "B", "C", "D", "E", "F", "G"])
    accids = set(["n", "d", "b", "#", "x"])

    debug = False
    debug_switch = input("Type D here for debug messages:")
    if debug_switch in ("D", "d"):
        debug = True

    while True:
        err = False
        part_of_pitch = 1
        note_name = ""
        accid = ""
        is_rational = False
        is_rational_used = False
        is_rational_ever_used = False
        in_numerator = False
        in_denominator = False
        is_neg_octave = False
        numerator = 0
        denominator = 1
        ratio = 0.0
        octave = 0
        pitch = input("\nPitches: ")

        # Parse inputted note
        if pitch in ("X", "x"):
            break
        curr_pitch = 0
        midi_note = []
        distance = []
        hz = []
        if debug:
            print("Parsing character by character ...")
        for c in pitch:
            if debug:
                print("char = %s, curr_pitch = %i, part_of_pitch = %i" %
                      (c, curr_pitch, part_of_pitch))

            if c == "":
                break
            if c == " ":
                if debug:
                    print("Advancing to next note.")
                curr_pitch += 1
                part_of_pitch = 0

            if part_of_pitch == 3:
                if c == "-":
                    is_neg_octave = True
                else:
                    try:
                        octave = int(("%i" + c) % octave)
                        if debug:
                            print("Octave assigned")
                    except ValueError:
                        print("Invalid format err 1")
                        err = True
                        break

                if err == True:
                    if debug:
                        print("Something just went wrong.")
                if err == False:
                    ratio = float(numerator) / denominator
                    if is_neg_octave:
                        octave = octave * (-1)
                    if debug:
                        print("--- Note name: " + note_name + " Accid: " +
                              accid + " Accid Ratio: %.3f Octave: %i" % (ratio, octave))

                    # Convert inputted note to MIDI note (possibly a rational number)
                    # C-1 = 0, C4 = 60, A4 = 69
                    diatonic_class = 0
                    pitch_class = 0
                    accid_value = 0.0
                    if note_name == "C":
                        diatonic_class = 0
                    if note_name == "D":
                        diatonic_class = 2
                    if note_name == "E":
                        diatonic_class = 4
                    if note_name == "F":
                        diatonic_class = 5
                    if note_name == "G":
                        diatonic_class = 7
                    if note_name == "A":
                        diatonic_class = 9
                    if note_name == "B":
                        diatonic_class = 11
                    if accid == "d":
                        accid_value = -2
                    if accid == "b":
                        accid_value = -1
                    if accid == "n":
                        accid_value = 0
                    if accid == "#":
                        accid_value = 1
                    if accid == "x":
                        accid_value = 2
                    if is_rational_used:
                        accid_value = accid_value * ratio

                    midi_note.append(
                        (diatonic_class + 12*(octave+1)) + accid_value)
                    # Convert MIDI note to Hz
                    # A4 = 69. Count semitones from A4.
                    midi_ref = 69  # The MIDI value for A4
                    distance.append(midi_note[curr_pitch] - midi_ref)
                    st_hz = 2**(1.0/12)
                    hz.append(a4_hz * (st_hz**(distance[curr_pitch])))

            if part_of_pitch == 2:
                if debug:
                    print("Detecting accidental ...")
                accid_success = False
                if c == ")":
                    is_rational = False
                    if debug:
                        print("Rational flag off")
                    accid_success = True
                if is_rational == False and c in accids:
                    if is_rational_used == False:
                        accid = c
                        if debug:
                            print("Accidental assigned")
                        part_of_pitch += 1
                        accid_success = True
                    if is_rational_used == True:
                        if c in set(["n", "d", "x"]):
                            print(
                                "Error: Only b and # accidentals are valid with rational accidentals.")
                            err = True
                            break
                        else:
                            accid = c
                            if debug:
                                print("Accidental assigned")
                            part_of_pitch += 1
                            accid_success = True
                if is_rational:
                    if in_denominator:
                        try:
                            denominator = int(c)
                            if debug:
                                print("Denominator assigned")
                            in_denominator = False
                            accid_success = True
                        except ValueError:
                            print("Invalid format err 2")
                            err = True
                            break
                    if c == "/":
                        in_numerator = False
                        in_denominator = True
                        accid_success = True
                    if in_numerator:
                        try:
                            numerator = int(c)
                            if debug:
                                print("Numerator assigned")
                            accid_success = True
                        except ValueError:
                            print("Invalid format err 3")
                            err = True
                            break
                if c == "(":
                    is_rational = True
                    is_rational_used = True
                    in_numerator = True
                    if debug:
                        print("Rational flag on.")
                    accid_success = True
                if accid_success == False:
                    print("Invalid format err 4")
                    err = True
                    break

            if part_of_pitch == 1:
                if c in note_names:
                    note_name = c
                    if debug:
                        print("Note name assigned.")
                    part_of_pitch += 1
                else:
                    print("Invalid format err 5")
                    err = True
                    break

            if part_of_pitch == 0:
                if is_rational_used:
                    is_rational_ever_used = True
                err = False
                part_of_pitch = 1
                note_name = ""
                accid = ""
                is_rational = False
                is_rational_used = False
                in_numerator = False
                in_denominator = False
                is_neg_octave = False
                numerator = 0
                denominator = 1
                ratio = 0.0
                octave = 0

        if is_rational_ever_used:
            # This syntax lifted from https://stackoverflow.com/questions/1566936/easy-pretty-printing-of-floats-in-python
            print("MIDI values: " + " ".join("%.2f" % n for n in midi_note))
            if debug:
                print("Semitone distances: " +
                      " ".join("%.2f" % n for n in distance))
        else:
            print("MIDI values: " + " ".join("%i" % n for n in midi_note))
            if debug:
                print("Semitone distances: " +
                      " ".join("%i" % n for n in distance))
        print("Hz values: " + " ".join("%.2f" % n for n in hz))
    top_menu()


def hz_to_pitch_tool():
    print("A4 = 440 assumed. Enter number as a decimal. Type X to quit.")

    while(True):
        pitch = ""
        midi_note = 0
        pitch_class_number = 0
        pitch_class_name = ""
        cents = 0.0
        octave = 0
        hz = input("\nHz: ")

        if hz in ("X", "x"):
            break

        try:
            # Ideally, fix bug where cents can be 100, e.g. C#4 + 100 c (which should read Dn4 + 0.0 c).
            hz = float(hz)
            midi_note = 12 * (math.log(hz/440.0, 2)) + 69
            print("MIDI value: %.3f" % midi_note)
            pitch_class = math.floor(midi_note) % 12
            if pitch_class == 0:
                pitch_class_name = "Cn"
            elif pitch_class == 1:
                pitch_class_name = "C#"
            elif pitch_class == 2:
                pitch_class_name = "Dn"
            elif pitch_class == 3:
                pitch_class_name = "Eb"
            elif pitch_class == 4:
                pitch_class_name = "En"
            elif pitch_class == 5:
                pitch_class_name = "Fn"
            elif pitch_class == 6:
                pitch_class_name = "F#"
            elif pitch_class == 7:
                pitch_class_name = "Gn"
            elif pitch_class == 8:
                pitch_class_name = "Ab"
            elif pitch_class == 9:
                pitch_class_name = "An"
            elif pitch_class == 10:
                pitch_class_name = "Bb"
            elif pitch_class == 11:
                pitch_class_name = "Bn"
            cents = 100 * (midi_note - math.floor(midi_note))
            octave = math.floor(midi_note/12.0) - 1
            print("Pitch name: " + pitch_class_name +
                  "%i + %.1f c" % (octave, cents))

        except ValueError:
            print("Not a decimal number.")
    top_menu()


def midi_to_pitch_tool():
    print("A4 = 440 assumed. Enter number as a decimal. Type X to quit.")

    while(True):
        midi_note = input("\nMIDI: ")

        if midi_note in ("X", "x"):
            break

        try:
            # Ideally, fix bug where cents can be 100, e.g. C#4 + 100 c (which should read Dn4 + 0.0 c).
            midi_note = float(midi_note)
            pitch_class = math.floor(midi_note) % 12
            if pitch_class == 0:
                pitch_class_name = "Cn"
            elif pitch_class == 1:
                pitch_class_name = "C#"
            elif pitch_class == 2:
                pitch_class_name = "Dn"
            elif pitch_class == 3:
                pitch_class_name = "Eb"
            elif pitch_class == 4:
                pitch_class_name = "En"
            elif pitch_class == 5:
                pitch_class_name = "Fn"
            elif pitch_class == 6:
                pitch_class_name = "F#"
            elif pitch_class == 7:
                pitch_class_name = "Gn"
            elif pitch_class == 8:
                pitch_class_name = "Ab"
            elif pitch_class == 9:
                pitch_class_name = "An"
            elif pitch_class == 10:
                pitch_class_name = "Bb"
            elif pitch_class == 11:
                pitch_class_name = "Bn"
            cents = 100 * (midi_note - math.floor(midi_note))
            octave = math.floor(midi_note/12.0) - 1
            print("Pitch name: " + pitch_class_name +
                  "%i + %.1f c" % (octave, cents))

            # Convert MIDI note to Hz
            # A4 = 69. Count semitones from A4.
            midi_ref = 69  # The MIDI value for A4
            distance = midi_note - midi_ref
            st_hz = 2**(1.0/12)
            hz = a4_hz * (st_hz**(distance))
            print("Hz value: %.3f" % hz)

        except ValueError:
            print("Not a decimal number.")

    top_menu()


def top_menu():
    print("\nMake a selection:\n(1) Pitch name to Hz (and MIDI).\n(2) Hz to pitch name.\n(3) MIDI to pitch name.\n(X) Exit.")
    choice = input("> ")
    if choice == "1":
        pitch_to_hz_tool()
    elif choice == "2":
        hz_to_pitch_tool()
    elif choice == "3":
        midi_to_pitch_tool()
    else:
        pass


def main():
    print("=== PITCH CONVERTER ===")
    print("Converts between different notations for pitch: Hz, MIDI, and pitch name.\n")
    a4_hz = input("Value for A4 in Hz (Press ENTER for default, A4=440)")
    if a4_hz == "":
        a4_hz = 440.0
    try:
        a4_hz = float(a4_hz)
    except ValueError:
        print("Press ENTER or input a number.")

    st_hz = 2**(1.0/12)
    print("Semitone Hz = {}".format(st_hz))

    top_menu()


if __name__ == "__main__":
    main()
