import unittest

from hz_convert.converters import assign_name, get_octave, get_cents_deviation, midi_to_hz

class TestMidiToPitch(unittest.TestCase):
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

    def test_get_cents_deviation_above_or_below(self):
        self.assertEqual(get_cents_deviation(120.4, 120), 40)
        self.assertEqual(get_cents_deviation(120.4, 121), 60)

    def test_get_cents_deviation_returns_decimals(self):
        self.assertEqual(get_cents_deviation(120.423, 121), 57.7)

        # Should round answer to 1 decimal place
        self.assertEqual(get_cents_deviation(120.4232, 121), 57.7)

    def test_midi_to_hz_normal_tuning(self):
        self.assertEqual(midi_to_hz(69, 440.0), 440.0)
        self.assertEqual(midi_to_hz(60, 440.0), 261.626)

    def test_midi_to_hz_different_tuning(self):
        self.assertEqual(midi_to_hz(69, 423.519), 423.519)
        self.assertEqual(midi_to_hz(60, 423.519), 251.826)



if __name__ == '__main__':
    unittest.main()
