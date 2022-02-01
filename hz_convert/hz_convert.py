#! /usr/bin/env python3

"""
Script to convert scientific pitch notation to Hz
Brad Gersh
"""

import converters


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

    top_menu(a4_hz)


def top_menu(a4_hz):
    while True:
        print("\nMake a selection:\n(1) Pitch name to Hz (and MIDI).\n(2) Hz to pitch name.\n(3) MIDI to pitch name.\n(X) Exit.")
        choice = input("> ")
        if choice == "1":
            converters.pitch_to_hz_tool(a4_hz)
        elif choice == "2":
            converters.hz_to_pitch_tool()
        elif choice == "3":
            converters.midi_to_pitch_tool()
        elif choice in ("X", "x"):
            break
        else:
            pass


if __name__ == "__main__":
    main()
