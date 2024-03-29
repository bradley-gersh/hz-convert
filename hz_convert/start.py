#! /usr/bin/env python3

#
# Script to convert scientific pitch notation to Hz
# Bradley Gersh
#

from sys import exit

from . import converters

def main():
    print('\n=== PITCH CONVERTER ===')
    print('Converts between different notations for equal-tempered pitch: Hz, MIDI, and pitch name.\n')

    try:
        a4_hz = set_a4()
        top_menu(a4_hz)
    except EOFError:
        print('test')
        exit()


def top_menu(a4_hz):
    while True:
        print('\nMake a selection:\n(1) Pitch name to Hz (and MIDI).\n(2) Hz to pitch name.\n(3) MIDI to pitch name.\n(X) Exit.')
        choice = input('> ')

        if choice == '1':
            converters.pitch_to_hz_loop(a4_hz)
        elif choice == '2':
            converters.hz_to_pitch_loop(a4_hz)
        elif choice == '3':
            converters.midi_to_pitch_loop(a4_hz)
        elif choice in ('X', 'x'):
            return True
        else:
            pass

def set_a4():
    a4_hz = input('> Input value for A4 in Hz (Press ENTER for default, A4=440): ')

    if a4_hz == '':
        return 440.0

    try:
        a4_hz = float(a4_hz)
    except ValueError:
        print('Invalid input. Using default A4=440.')
        a4_hz = 440.0

    return a4_hz


if __name__ == '__main__':
    main()
