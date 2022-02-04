# Hz Convert

This Python package converts mutually between sine-tone frequencies (Hz), MIDI
pitch numbers, and pitch names in scientific pitch notation (e.g. "E-flat 4").
It handles microtones in both input and output and can allow for A4 to be
tuned to a non-standard frequency. The package can be imported into other
projects or used as a standalone application from the command line.

## Usage

Python 3 is required (ideally at least 3.7). Download and unzip the repository,
then from the top of the unzipped directory, follow one of the usage options
below.

### 1. Using as an interactive script

This method is suggested if you want to use the script as a simple calculator.
It allows you to enter strings of input and receive the conversions between
pitch names, MIDI values, and frequencies (Hz).

From the top of project directory, execute from the command line:

```bash
python hz_convert.py
```

You will be asked to set a reference point for the note A4 (default is
A4 = 440 Hz), then to select the type of conversion you want. Specific
instructions for each conversion are given after you select a type; see below
for more details. Each converter accepts individual values or a space-delimited
series of values.

At any time, type `x` to return to the main menu and `x` again to exit. `Ctrl-D`
will also exit gracefully.

#### Sample use as interactive script

In each case, the line beginning `>` accepts user input after the `:`. The lines
beginning `-` are returned by the script.

1. From pitch names. The pitch-name format is described below.

  ```txt
  > Pitches: C4 D#3 E(1/2)b-1
  - MIDI values: 60.00, 51.00, 3.50
  - Hz values: 261.63, 155.56, 10.01
  ```

2. From frequency values. All entries must be greater than 0.

  ```txt
  > Hz: 2418 28.24 514
  - Pitch names: D7 (+49.9 c), A0 (+46.0 c), C4 (-30.9 c)
  - MIDI values: 98.50, 21.46, 71.69
  ```

3. From MIDI numbers. Floating point numbers and values outside
the standard 0-127 range are accepted.

  ```txt
  > MIDI: 60 24.33 -3 138
  - Pitch names: C4 (+0.0 c), C1 (+33.0 c), A-2 (+0.0 c), F#10 (+0.0 c)
  - Hz values: 261.63, 33.33, 6.88, 23679.64
  ```

### 2. Using as a package

#### Installation

This method is suggested if you wish to incorporate the conversions into another
Python program or script. Using the package manager `pip`, you can install the `hz_convert` package to your Python environment by navigating to the top folder
of this repository and executing

```bash
pip install .
```

- If you are using `pip` version 21 or lower, you may receive a message
  prompting you to use the command `pip install .
  --use-feature=in-tree-build` instead.
- If you wish to modify the source and use the changes without reinstalling
  each time, add the `-e` option: `pip install . -e`
- To uninstall, call `pip uninstall hz_convert`.

From within a Python REPL or script, you can then import the package:

```python
import hz_convert
```

#### Features

Pitches are represented by the `Pitch` dataclass, which has the following
fields:

- `name`: A human-readable name for the pitch as a string, like
`'Bb4 (+2.0 c)'`.
- `diatonic_pc`: The diatonic letter name, one of `A`, `B`, `C`, `D`, `E`, `F`,
  `G`.
- `accidental`: Can be one of `b` (flat), `#` (sharp), `n` or `''` (natural),
  `d` (double flat), or `#` (double sharp).
- `octave`: An integer for the octave in scientific notation, where octave 4
  runs from middle C (`C4`) to the B on the treble staff (`B4`).
- `cents_dev`: A float representing the microtonal shift in cents from the
  chromatic pitch indicated by `diatonic_pc` and `accidental`.

The package exposes three primary functions:

- `from_midi(input, a4_hz=440.0)`: Accepts a number (`int` or `float`), list of
  numbers, or space-delimited string of numbers representing the MIDI values to
  convert. Values can be outside the 0-127 range of standard MIDI.
- `from_hz(input, a4_hz=440.0)`: Accepts a number (`int` or `float`), list of
  numbers, or space-delimited string of numbers representing the frequencies
  (Hz) to convert. Input values must be greater than 0.
- `from_pitch(input, a4_hz=440.0)`: Accepts a list of strings or one
  space-delimited string containing pitch names to convert to MIDI or frequency
  (Hz) values. See description of the pitch-name format below.

Each function takes an optional second argument that specifies which frequency
is assigned to A4 (default 440.0). Note that this only affects computations
to and from frequency values (Hz).  The correspondence between MIDI numbers and
pitch names does not change if A4 is set to a different frequency.

Each function returns a dictionary of the following form:

```python
{
    'hz': list[float],          # Frequency values (Hz) of the entered pitches
    'midi': list[float],        # MIDI values of the entered pitches
    'pitch': list[Pitch],       # Pitch objects for the entered pitches
    'pitch_names': list[str],   # List of human-readable pitch names
    'a4': float                 # The value of A4 used for computing frequencies
}
```

The package also exposes the `main()` method, which runs the same interactive
script as calling `python hz_convert.py` from the command line.

#### Sample use as package

```python
import hz_convert as hc

x = hc.from_midi([60, 67, 52.39, 150, -4.3])         # Using a list as input
y = hc.from_hz([249, 424.24, 86, 7712], a4_hz=444.2) # Changing the value of A4
z = hc.from_pitch('C4 Bb3 A-1 Gx2 E(2/3)b6')         # Using a string as input

'''
One returned value:

x = {
    'hz': [261.626, 391.995, 168.569, 47359.286, 6.378],
    'midi': [60, 67, 52.39, 150, -4.3],
    'pitch': [
        Pitch(name='C4 (+0.0 c)', diatonic_pc='C', accidental='', octave=4, cents_dev=0.0)
        # ... and four others
      ],
    'pitch_names': [
        'C4 (+0.0 c)', 'G4 (+0.0 c)', 'E3 (+39.0 c)', 'F#11 (+0.0 c)', 'G#-2 (-30.0 c)'],
    'a4': 440.0
}
'''
```

## Pitch names

All pitch names are strings that follow the format `letter_name (microtone) accidental octave` (without spaces), such as `C4`, `An4`, `Eb2`, `Gx7`, `Dd2`, `B(4/9)#0`,
`F-2`, `C(8/3)b-3`. The different parts each have restrictions for valid input:

- `letter_name`: A capital letter from `A` through `G`.
- `microtone` (optional): A fraction of one semitone, represented as two
positive integers surrounded by parentheses, such as `(1/3)`. Microtones
greater than `1`, such as `(3/2)`, are accepted. If a value for `microtone` is
included, the following `accidental` must be `b` or `#`.

  **Caution!** The fraction in `microtone` is taken of one *semitone*. This
  corresponds to cents usage but not to customary usage, which considers
  fractions of *whole tones* relative to the diatonic pitches of C major.
  Customarily, for example, "D two-thirds-flat 3" is two-thirds of the way from
  D3 toward C3, so it is lower than D-flat 3. In our notation, however,
  `'D(2/3)b3'` represents the pitch two-thirds of the way from D3 toward
  D-flat 3 and is higher than D-flat 3.

  In practice, this means that the conventional microtone name must be
  multiplied by 2 for the fraction used in `microtone`. The name `'D(2/3)b3'`
  is commonly called the "(one-)third tone below D3," and "D two-thirds-flat 3"
  is represented `'D(4/3)b3'`.

- `accidental`: One of `b` (flat), `#` (sharp), `n` or `''` (natural), `d`
(double flat), or `x` (double sharp). Assumed to be natural if omitted.
- `octave`: An integer. Negative integers are allowed but should not be
surrounded by parentheses. For example, MIDI note `1` corresponds to `'C#-1'`.


## Testing

This repo comes with a testing suite of unit and integration tests in the `test`
folder. To run it, from the top-level folder execute the command

```bash
python -m unittest
```

## License and Contact

(c) 2021-2022 Bradley Gersh. This repository is released under the MIT license.
Please feel free to use with attribution, and contact me with any suggestions!
