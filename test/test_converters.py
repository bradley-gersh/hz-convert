import unittest
from unittest import mock
from io import StringIO

import hz_convert.converters as c

A4_HZ = 440.0

class TestHzToPitchLoop(unittest.TestCase):
    def test_exits_normally(self):
        with mock.patch('builtins.input', side_effect=['X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.hz_to_pitch_loop(A4_HZ))

    def test_good_input(self):
        with mock.patch('builtins.input', side_effect=['440.0003', '261.62559', '29.989', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.hz_to_pitch_loop(A4_HZ))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertListEqual(out[0:2], ['- Pitch name: An4 + 0.0 c', '- MIDI value: 69'])
            self.assertListEqual(out[2:4], ['- Pitch name: Cn4 + 0.0 c', '- MIDI value: 60'])
            self.assertListEqual(out[4:6], ['- Pitch name: Bb0 + 50.0 c', '- MIDI value: 22.50'])

    def test_broken_input(self):
        with mock.patch('builtins.input', side_effect=['not a number', 'x']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(A4_HZ))
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, 'Not a decimal number. Type X to quit.')

class TestHzToMidi(unittest.TestCase):
    def test_converts_correctly(self):
        self.assertEqual(c.hz_to_midi(440.0, 440.0), 69.0)
        self.assertEqual(c.hz_to_midi(261.626, 440.0), 60.0)
        self.assertEqual(c.hz_to_midi(443.0, 443.0), 69.0)

class TestMidiToPitchLoop(unittest.TestCase):
    def test_exits_normally(self):
        with mock.patch('builtins.input', side_effect=['X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(A4_HZ))

    def test_good_input(self):
        with mock.patch('builtins.input', side_effect=['69', '22.5', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(A4_HZ))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertTrue('- Pitch name: An4 + 0.0 c' in out)
            self.assertTrue('- Hz value: 440.000' in out)
            self.assertTrue('- Pitch name: Bb0 + 50.0 c' in out)
            self.assertTrue('- Hz value: 29.989' in out)

    def test_broken_input(self):
        with mock.patch('builtins.input', side_effect=['not a number', 'x']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(A4_HZ))
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, 'Not a decimal number. Type X to quit.')

class TestMidiToPitch(unittest.TestCase):
    def test_good_input(self):
        with mock.patch('hz_convert.converters.get_cents_dev_direction', \
                    side_effect=['+', '-']), \
                mock.patch('hz_convert.converters.assign_name', side_effect=['An', 'D#']), \
                mock.patch('hz_convert.converters.get_cents_dev', side_effect=[23.2, 43.1]), \
                mock.patch('hz_convert.converters.get_octave', side_effect=[3, 5]):

            pitch1 = c.midi_to_pitch(57.232)
            pitch2 = c.midi_to_pitch(75.569)

            self.assertListEqual([
                pitch1.pitch_class_name,
                pitch1.octave,
                pitch1.cents_dev_direction,
                pitch1.cents_dev
            ], ['An', 3, '+', 23.2])

            self.assertListEqual([
                pitch2.pitch_class_name,
                pitch2.octave,
                pitch2.cents_dev_direction,
                pitch2.cents_dev
            ], ['D#', 5, '-', 43.1])

class TestOutputs(unittest.TestCase):
    def test_hz_string_one_good_input(self):
        self.assertEqual(c.hz_string(440.0), '- Hz value: 440.000')
        self.assertEqual(c.hz_string(261.626), '- Hz value: 261.626')
        self.assertEqual(c.hz_string(730.184), '- Hz value: 730.184')

    def test_hz_string_many_good_inputs(self):
        self.assertEqual(c.hz_string([440, 323.4445, 289.2]), '- Hz values: 440.000, 323.445, 289.200')

    def test_hz_string_bad_input(self):
        with self.assertRaises(TypeError), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            c.hz_string([240.5, 'invalid Hz value'])
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, '[BUG] Invalid pitch class number.')

    def test_pitch_string_good_input(self):
        pitches = [
            c.Pitch('An', 3, '+', 23.2),
            c.Pitch('D#', 5, '-', 43.1)
        ]

        self.assertEqual(c.pitch_string(pitches[0]), '- Pitch name: An3 + 23.2 c')
        self.assertEqual(c.pitch_string(pitches[1]), '- Pitch name: D#5 - 43.1 c')

    def test_midi_string_one_good_input(self):
        self.assertEqual(c.midi_string(60.20, microtonal = False), '- MIDI value: 60')
        self.assertEqual(c.midi_string(52.00, microtonal = True), '- MIDI value: 52.00')

    def test_midi_string_many_good_inputs(self):
        self.assertEqual(c.midi_string([60.20, 43.9, 15], microtonal = False), '- MIDI values: 60, 43, 15')
        self.assertEqual(c.midi_string([60.20, 43.9, 15], microtonal = True), '- MIDI values: 60.20, 43.90, 15.00')

    def test_midi_string_broken_input(self):
        with self.assertRaises(TypeError), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            c.midi_string([34, 'invalid value'])
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, 'MIDI values must be numerical.')


class TestMidiToPitchHelpers(unittest.TestCase):
    def test_assign_name_to_Cn(self):
        self.assertEqual(c.assign_name(0), 'Cn')
        self.assertEqual(c.assign_name(8), 'G#')
        self.assertEqual(c.assign_name(10), 'Bb')

    def test_assign_name_fails_out_of_range(self):
        with self.assertRaises(KeyError), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            c.assign_name(12)
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, '[BUG] Invalid pitch class number.')

    def test_get_octave(self):
        self.assertEqual(c.get_octave(60), 4)
        self.assertEqual(c.get_octave(59), 3)
        self.assertEqual(c.get_octave(73), 5)

    def test_get_cents_dev_direction(self):
        self.assertEqual(c.get_cents_dev_direction(45), '+')
        self.assertEqual(c.get_cents_dev_direction(45.01), '+')
        self.assertEqual(c.get_cents_dev_direction(45.49), '+')
        self.assertEqual(c.get_cents_dev_direction(45.50), '+')
        self.assertEqual(c.get_cents_dev_direction(45.51), '-')
        self.assertEqual(c.get_cents_dev_direction(45.99), '-')
        self.assertEqual(c.get_cents_dev_direction(46), '+')

    def test_get_cents_dev_above_or_below(self):
        self.assertEqual(c.get_cents_dev(120.4, 120), 40)
        self.assertEqual(c.get_cents_dev(120.4, 121), 60)

    def test_get_cents_dev_returns_decimals(self):
        self.assertEqual(c.get_cents_dev(120.423, 121), 57.7)

        # Should round answer to 1 decimal place
        self.assertEqual(c.get_cents_dev(120.4232, 121), 57.7)

    def test_midi_to_hz_normal_tuning(self):
        self.assertEqual(c.midi_to_hz(69, 440.0), 440.0)
        self.assertEqual(c.midi_to_hz(60, 440.0), 261.626)
        self.assertEqual(c.midi_to_hz(78.43, 440.0), 758.599)

    def test_midi_to_hz_different_tuning(self):
        self.assertEqual(c.midi_to_hz(69, 423.519), 423.519)
        self.assertEqual(c.midi_to_hz(60, 423.519), 251.826)
        self.assertEqual(c.midi_to_hz(78.43, 423.519), 730.184)


if __name__ == '__main__':
    unittest.main()
