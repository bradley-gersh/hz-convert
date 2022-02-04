# Hz Convert

This Python package helps you convert between sine-tone frequencies (Hz), MIDI
pitch numbers, and pitch names in scientific pitch notation (e.g. "E-flat 4").
It allows you to set a custom tuning for A4, and it can handle microtones in
both input and output. It can be used as a package imported into other scripts
or as a standalone application.

## Usage

Python 3 is required, ideally at least 3.7. First, download the repository and
unzip it to some directory. Navigate into that directory, then follow one of the
two usage options below.

### 1. Using as a script

This method is suggested if you want to use the script as a simple calculator.
It allows you to enter strings of input and receive the conversions between
pitch names, MIDI values, and frequencies (Hz).

From the command line, navigate into the top of project directory and execute:

```bash
python hz_convert.py
```

You will be asked to set a reference point for the note A4 (default is
A4 = 440 Hz), then to select the type of conversion you want from a menu.
Specific instructions for each conversion are given after you select a type.
Each converter accepts individual values or a space-delimited series of values.

At any time, type `x` to return to the main menu and `x` again to exit.

#### Sample entries

1. From pitch names:

  ```txt
  > Pitches: C4 D#3 E(1/2)b-1
  - MIDI values: 60.00, 51.00, 3.50
  - Hz values: 261.63, 155.56, 10.01
  ```

2. From Hz values:

  ```txt
  > Hz: 2418 28.24 514
  - Pitch names: D7 (+49.9 c), A0 (+46.0 c), C4 (-30.9 c)
  - MIDI values: 98.50, 21.46, 71.69
  ```

3. From MIDI numbers, including decimals and numbers outside the 0-127 range:

  ```txt
  > MIDI: 60 24.33 -3 138
  - Pitch names: C4 (+0.0 c), C1 (+33.0 c), A-2 (+0.0 c), F#10 (+0.0 c)
  - Hz values: 261.63, 33.33, 6.88, 23679.64
  ```

### 2. Using as a package

#### Installation

This method is suggested if you wish to incorporate the conversions into some
larger Python program or script. Using the package manager `pip`, from the top
folder in this directory you can type

```bash
pip install .
```

to install the `hz_convert` package in your Python environment.

- If you are using `pip` version 21 or lower, you may receive a message
  prompting you to instead use the command `pip install .
  --use-feature=in-tree-build` .
- If you wish to modify the source and use the changes without reinstalling
  each time, use the `-e` option: `pip install . -e`

From within a Python REPL or script, you can then import the package:

```python
import hz_convert
```

#### Features

Pitches are represented by the `Pitch` dataclass, which has the following
fields:

- `name`: A human-readable name for the pitch as a string, like `'Bb4 (+2.0 c)`.
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
- `from_pc(input, a4_hz=440.0)`: Accepts a list of strings or one
  space-delimited string containing pitch names to convert to MIDI or frequency
  (Hz) values.

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

## Testing

This repo comes with a testing suite that includes both unit and integration
tests, located in the `test` folder. To run it, from the top-level folder run
the command

```bash
python -m unittest
```

Discovery mode should load the tests automatically (currently 57).

## License and Contact

(c) 2021-2022 Bradley Gersh. This repository is released under the MIT license.
Please attribute and feel free to use. Contact me with any suggestions!
