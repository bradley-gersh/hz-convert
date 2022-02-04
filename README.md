# Hz Convert

This Python package helps you convert between sine-tone frequencies (Hz), MIDI
pitch numbers, and pitch names in scientific pitch notation (e.g. "E-flat 4").
It can be used as a package imported into other scripts or as a standalone
application.

## Usage

Python 3 is required, ideally at least 3.7. First, download the repository and
unzip it to some directory. Navigate into that directory, then follow one of the
two usage options below.

### 1. Using as a script

From the command line, navigate into the top of project directory and execute:

```bash
python hz_convert.py
```

You will be asked to set a reference point for the note A4 (default is
A4 = 440 Hz), then to select the type of conversion you want from a menu.
Specific instructions for each conversion are given after you select a type.

At any time, type `x` to return to the main menu and `x` again to exit.

### Using as a package

Using the package manager `pip` (version at least 22.0.0 recommended), from the
top folder in this directory you can type

```bash
pip install .
```

to install the `hz_convert` package in your Python environment. Then, from
within the Python REPL or a script, you can import the package:

```python
import hz_convert
```


## Testing

This repo comes with a testing suite that includes both unit and integration tests,
located in the `test` folder. To run it, from the top-level folder run the command

```bash
python -m unittest
```

Discovery mode should load the tests automatically (currently 57).

## License and Contact

This repository is released under the MIT license. Please attribute and feel
free to use. Contact me with any suggestions!
