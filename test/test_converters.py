import unittest
from unittest import mock

from hz_convert.converters import midi_to_pitch_loop, midi_to_pitch, midi_to_pitch_string, assign_name, get_octave, get_cents_dev, get_cents_dev_direction, midi_to_hz, midi_to_hz_string

A4_HZ = 440.0

class TestMidiToPitchLoop(unittest.TestCase):
    def test_loop_exits(self):
        with mock.patch('builtins.input', side_effect=['x']):
            self.assertTrue(midi_to_pitch_loop(A4_HZ))

    def test_midi_to_pitch(self):
        with \
            mock.patch('hz_convert.converters.get_cents_dev_direction', side_effect=['+', '-']), \
            mock.patch('hz_convert.converters.assign_name', side_effect=['An', 'D#']), \
            mock.patch('hz_convert.converters.get_cents_dev', side_effect=[23.2, 43.1]), \
            mock.patch('hz_convert.converters.get_octave', side_effect=[3, 5]):

            self.assertDictEqual(midi_to_pitch(57.232), {
                'pitch_class_name': 'An',
                'octave': 3,
                'cents_dev_direction': '+',
                'cents_dev': 23.2
            })
            self.assertDictEqual(midi_to_pitch(74.569), {
                'pitch_class_name': 'D#',
                'octave': 5,
                'cents_dev_direction': '-',
                'cents_dev': 43.1
            })

    def test_midi_to_pitch_string(self):
        pitches = [
            {
                'pitch_class_name': 'An',
                'octave': 3,
                'cents_dev_direction': '+',
                'cents_dev': 23.2
            },
            {
                'pitch_class_name': 'D#',
                'octave': 5,
                'cents_dev_direction': '-',
                'cents_dev': 43.1
            }
        ]

        with mock.patch('hz_convert.converters.midi_to_pitch', side_effect=pitches):
            self.assertEqual(midi_to_pitch_string(57.232), 'Pitch name: An3 + 23.2 c')
            self.assertEqual(midi_to_pitch_string(74.569), 'Pitch name: D#5 - 43.1 c')

class TestMidiToPitchHelpers(unittest.TestCase):
    def test_assign_name_to_Cn(self):
        self.assertEqual(assign_name(0), 'Cn')
        self.assertEqual(assign_name(8), 'G#')
        self.assertEqual(assign_name(10), 'Bb')

    def test_assign_name_fails_out_of_range(self):
        with self.assertRaises(KeyError):
            assign_name(12)

    def test_get_octave(self):
        self.assertEqual(get_octave(60), 4)
        self.assertEqual(get_octave(59), 3)
        self.assertEqual(get_octave(73), 5)

    def test_get_cents_dev_direction(self):
        self.assertEqual(get_cents_dev_direction(45), '+')
        self.assertEqual(get_cents_dev_direction(45.01), '+')
        self.assertEqual(get_cents_dev_direction(45.49), '+')
        self.assertEqual(get_cents_dev_direction(45.50), '+')
        self.assertEqual(get_cents_dev_direction(45.51), '-')
        self.assertEqual(get_cents_dev_direction(45.99), '-')
        self.assertEqual(get_cents_dev_direction(46), '+')

    def test_get_cents_dev_above_or_below(self):
        self.assertEqual(get_cents_dev(120.4, 120), 40)
        self.assertEqual(get_cents_dev(120.4, 121), 60)

    def test_get_cents_dev_returns_decimals(self):
        self.assertEqual(get_cents_dev(120.423, 121), 57.7)

        # Should round answer to 1 decimal place
        self.assertEqual(get_cents_dev(120.4232, 121), 57.7)

    def test_midi_to_hz_normal_tuning(self):
        self.assertEqual(midi_to_hz(69, 440.0), 440.0)
        self.assertEqual(midi_to_hz(60, 440.0), 261.626)
        self.assertEqual(midi_to_hz(78.43, 440.0), 758.599)

    def test_midi_to_hz_different_tuning(self):
        self.assertEqual(midi_to_hz(69, 423.519), 423.519)
        self.assertEqual(midi_to_hz(60, 423.519), 251.826)
        self.assertEqual(midi_to_hz(78.43, 423.519), 730.184)

    def test_midi_to_hz_string(self):
        with mock.patch('hz_convert.converters.midi_to_hz', side_effect = [440, 261.62556, 730.18399]):
            self.assertEqual(midi_to_hz_string(69, 440.0), 'Hz value: 440.000')
            self.assertEqual(midi_to_hz_string(60, 440.0), 'Hz value: 261.626')
            self.assertEqual(midi_to_hz_string(78.43, 423.519), 'Hz value: 730.184')

if __name__ == '__main__':
    unittest.main()
