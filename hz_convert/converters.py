import math
import re
from dataclasses import dataclass

# Constants
OCTAVE_DIV = 12
ST_HZ = 2**(1.0/OCTAVE_DIV)
MIDI_REF = 69 # An4
START_CHAR = '- '

@dataclass
class Pitch():
    pitch_class_name: str
    octave: int
    cents_dev_direction: str
    cents_dev: float

# Interaction loops
def pitch_to_hz_loop(a4_hz):
    print('A4 = %.3f Hz' % a4_hz)
    print("\nEnter a list of pitches in scientific pitch notation (separated by spaces) press ENTER. Format is pitch name (A-G), accidental (see next), and octave (an integer), all without spaces. Examples: Cn4, Bb8, F#4.\n")
    print("Accidentals can be #, b, or n (natural). Double sharps and flats are indicated by x and d (a single-character version of double flat). Rational accidentals are indicated by a fraction before the accidental in parens, e.g. (1/4)#, (2/3)b. Accidentals MAY NOT BE OMITTED. e.g. B(3/4)#8.\n")
    print("\nWARNING: Quarter tones are indicated by HALF accidentals. This is because accidentals themselves already embed semitones. Thus a quarter tone above Cn4 is C 'half sharp', or C(1/2)#4.\n\nExample input: Cn4 D#6 B(1/2)b3")

    print('\nType X to quit.')

    while True:
        pitch_in = input('\n> Pitches: ')

        if pitch_in in ('X', 'x'):
            return True

        pitches = pitch_in.split(' ')

        try:
            midi_notes = [pitch_str_to_midi(pitch) for pitch in pitches]
            hz = [midi_to_hz(float(midi_note), a4_hz) for midi_note in midi_notes]
            microtonal = any([midi_note % 1 != 0 for midi_note in midi_notes])
        except Exception as e:
            print('[error] ' + e)
        else:
            print(midi_string(midi_notes, microtonal))
            print(hz_string(hz))

def hz_to_pitch_loop(a4_hz):
    print('Enter number as a decimal. Type X to quit.\n')

    while(True):
        hz_in = input('\n> Hz: ')

        if hz_in in ('X', 'x'):
            return True

        hzs = hz_in.split(' ')

        try:
            midi_notes = [hz_to_midi(float(hz), a4_hz) for hz in hzs]
            pitch_data = [midi_to_pitch(midi_note) for midi_note in midi_notes]
            microtonal = any([midi_note % 1 != 0 for midi_note in midi_notes])
        except ValueError:
            print('[error] Not a decimal number. Type X to quit.\n')
            continue
        except KeyError:
            continue
        else:
            print(pitch_string(pitch_data))
            print(midi_string(midi_notes, microtonal))


def midi_to_pitch_loop(a4_hz):
    print('Enter MIDI number as an integer or decimal number. Type X to quit.\n')

    while(True):
        midi_in = input('\n> MIDI: ')

        if midi_in in ('X', 'x'):
            return True

        midi_notes = midi_in.split(' ')

        try:
            pitches = [midi_to_pitch(float(midi_note)) for midi_note in midi_notes]
            hzs = [midi_to_hz(float(midi_note), a4_hz) for midi_note in midi_notes]
        except ValueError:
            print('Not a decimal number. Type X to quit.')
            continue
        except KeyError:
            continue

        print(pitch_string(pitches))
        print(hz_string(hzs))

# Conversion functions
def pitch_str_to_midi(pitch_str):
    midi = -1

    pitch_name_format = '([a-gA-G])'
    microtone_format = '(\(([0-9]+)\/([0-9]+)\))'
    accidental_format = '([nb#xd])'
    octave_format = '(-?[0-9]+)'

    pitch_format = pitch_name_format + microtone_format + '?' + \
                   accidental_format + '?' + octave_format

    match = re.fullmatch(pitch_format, pitch_str)

    if not match:
        raise ValueError('[error] Invalid pitch format. Refer to instructions.\n')

    (pitch_name, numerator, denominator, accidental, octave) = match.group(1, 3, 4, 5, 6)

    if numerator is not None and denominator is not None:
        cents_dev = microtone_to_cents_dev(accidental, numerator, denominator)
    else:
        cents_dev = 0

    pitch = Pitch(pitch_name, int(octave), '+', float(cents_dev))
    midi = pitch_obj_to_midi(pitch)

    return midi

def microtone_to_cents_dev(accidental, numerator, denominator):
    if (accidental not in ('b', '#')):
        raise ValueError('[error] Only # and b are possible with microtones.')
    ratio = float(numerator) / float(denominator)
    accidental_value = accidental_to_value(accidental) * ratio

    return accidental_value * 100

def accidental_to_value(accidental):
    accidental_values = {
        'd': -2,
        'b': -1,
        'n': 0,
        '#': 1,
        'x': 2
    }

    if accidental == '':
        accidental = 'n'

    try:
        accidental_value = accidental_values[accidental]
    except KeyError:
        raise KeyError('[error] Invalid accidental type.\n')
    else:
        return accidental_value

def pitch_obj_to_midi(pitch):
    diatonic_class = assign_diatonic_pc(pitch.pitch_class_name)
    midi_note = round(diatonic_class + OCTAVE_DIV * (pitch.octave + 1) + pitch.cents_dev / 100, 2)

    return midi_note


def midi_to_pitch(midi_note):
    cents_dev_direction = get_cents_dev_direction(midi_note)
    rounded_pitch = round(midi_note)
    pitch_class_name = assign_name(rounded_pitch % 12)
    cents_dev = get_cents_dev(midi_note, rounded_pitch)
    octave = get_octave(midi_note)

    return Pitch(pitch_class_name, octave, cents_dev_direction, cents_dev)

def hz_to_midi(hz, a4_hz):
    return round(OCTAVE_DIV * (math.log(hz / a4_hz, 2)) + MIDI_REF, 3)

def midi_to_hz(midi_note, a4_hz):
    distance = midi_note - MIDI_REF
    return round(a4_hz * (ST_HZ**distance), 3)

# Output functions
def pitch_string(pitches):
    if type(pitches) is not list:
        pitches = [pitches]

    if len(pitches) > 1:
        prefix = 'Pitch names: '
    else:
        prefix = 'Pitch name: '

    try:
        out_str = START_CHAR + prefix + ', '.join([pitch.pitch_class_name + \
            '%i ' % pitch.octave + pitch.cents_dev_direction + \
            ' %.1f c' % pitch.cents_dev for pitch in pitches])
    except TypeError:
        raise TypeError('[error] Unable to process pitch string data.')
    else:
        return out_str

def hz_string(hzs):
    if type(hzs) is not list:
        hzs = [hzs]

    if len(hzs) > 1:
        prefix = 'Hz values: '
    else:
        prefix = 'Hz value: '

    try:
        out_str = START_CHAR + prefix + ', '.join('%.3f' % hz for hz in hzs)
    except TypeError:
        raise TypeError("[error] Hz values must be floats.")
    else:
        return out_str

def midi_string(midi_notes, microtonal = False):
    if type(midi_notes) is not list:
        midi_notes = [midi_notes]

    if len(midi_notes) > 1:
        prefix = 'MIDI values: '
    else:
        prefix = 'MIDI value: '

    num_format = '%.2f' if microtonal else '%i'

    try:
        out_str = START_CHAR + prefix + ', '.join(num_format % midi_note for midi_note in midi_notes)
    except TypeError:
        raise TypeError("[error] MIDI values must be numerical.")
    else:
        return out_str

# Helper functions
def assign_name(pitch_class):
    pc_names = {
        0: 'Cn',
        1: 'C#',
        2: 'Dn',
        3: 'Eb',
        4: 'En',
        5: 'Fn',
        6: 'F#',
        7: 'Gn',
        8: 'G#',
        9: 'An',
        10: 'Bb',
        11: 'Bn'
    }

    try:
        pc_name = pc_names[pitch_class]
    except KeyError:
        raise KeyError('[BUG] Invalid pitch class number')
    else:
        return pc_name

def assign_diatonic_pc(name):
    diatonic_pc_numbers = {
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11
    }

    try:
        diatonic_pc_number = diatonic_pc_numbers[name.upper()]
    except KeyError:
        raise KeyError('[BUG] Invalid pitch class name')
    else:
        return diatonic_pc_number

def get_cents_dev_direction(midi_note):
    return '+' if (midi_note % 1) <= 0.5 else '-'

def get_cents_dev(midi_note, pitch_class_number):
    return round(100 * abs(midi_note - pitch_class_number), 1)

def get_octave(midi_note):
    return math.floor(midi_note/12.0) - 1
