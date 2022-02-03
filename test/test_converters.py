import unittest
from unittest import mock
from io import StringIO

import hz_convert.converters as c

STD_A4 = 440.0
NEW_A4 = 423.519

def compare_pitch_objs(pitch1, pitch2):
    return ((pitch1.diatonic_pc == pitch2.diatonic_pc) and \
        (pitch1.accidental == pitch2.accidental) and \
        (pitch1.octave == pitch2.octave) and \
        (pitch1.cents_dev == pitch2.cents_dev))

# The three loops have integration tests without mocking subroutines
class TestPitchToHzLoop(unittest.TestCase):
    def test_exits_normally(self):
        with mock.patch('builtins.input', side_effect=['X']), \
                mock.patch('sys.stdout'):
            self.assertTrue(c.pitch_to_hz_loop(STD_A4))

    def test_good_input_standard_a4(self):
        with mock.patch('builtins.input', side_effect=['An4', 'Cn4 B(1/2)b0', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.pitch_to_hz_loop(STD_A4))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertListEqual(out[0:2], ['- MIDI value: 69', '- Hz value: 440.00'])
            self.assertListEqual(out[2:4], ['- MIDI values: 60.00, 22.50', '- Hz values: 261.63, 29.99'])

    def test_good_input_new_a4(self):
        with mock.patch('builtins.input', side_effect=['An4', 'Cn4 B(1/2)b0', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.pitch_to_hz_loop(NEW_A4))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertListEqual(out[0:2], ['- MIDI value: 69', '- Hz value: 423.52'])
            self.assertListEqual(out[2:4], ['- MIDI values: 60.00, 22.50', '- Hz values: 251.83, 28.87'])

    def test_broken_input(self):
        with mock.patch('builtins.input', side_effect=['not a number', 'x']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.pitch_to_hz_loop(STD_A4))
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, "[error] Syntax error: Invalid pitch format. At minimum, a pitch and octave (e.g. 'C4', 'Bb3') are required. Refer to instructions.")

class TestHzToPitchLoop(unittest.TestCase):
    def test_exits_normally(self):
        with mock.patch('builtins.input', side_effect=['X']), \
                mock.patch('sys.stdout'):
            self.assertTrue(c.hz_to_pitch_loop(STD_A4))

    def test_good_input_standard_a4(self):
        with mock.patch('builtins.input', side_effect=['440.0003', '261.62559 29.989', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.hz_to_pitch_loop(STD_A4))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertListEqual(out[0:2], ['- Pitch name: A4 (+0.0 c)', '- MIDI value: 69'])
            self.assertListEqual(out[2:4], ['- Pitch names: C4 (+0.0 c), Bb0 (+50.0 c)', '- MIDI values: 60.00, 22.50'])

    def test_good_input_new_a4(self):
        with mock.patch('builtins.input', side_effect=['440.0003', '261.62559 29.989', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.hz_to_pitch_loop(NEW_A4))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertListEqual(out[0:2], ['- Pitch name: Bb4 (-33.9 c)', '- MIDI value: 69.66'])
            self.assertListEqual(out[2:4], ['- Pitch names: C#4 (-33.9 c), B0 (+16.1 c)', '- MIDI values: 60.66, 23.16'])

    def test_broken_input(self):
        with mock.patch('builtins.input', side_effect=['not a number', 'x']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(STD_A4))
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, '[error] Syntax error: Not a numerical input.')

class TestPitchToMidi(unittest.TestCase):
    # This function is basically a wrapper for two other functions,
    # so here it receives an integration test.

    def test_handles_simple_input(self):
        self.assertEqual(c.pitch_str_to_midi('An4'), 69.0)
        self.assertEqual(c.pitch_str_to_midi('C4'), 60.0)
        self.assertEqual(c.pitch_str_to_midi('Bb5'), 82.0)
        self.assertEqual(c.pitch_str_to_midi('F#2'), 42.0)

    def test_handles_negative_octaves(self):
        self.assertEqual(c.pitch_str_to_midi('Bn-1'), 11.0)
        self.assertEqual(c.pitch_str_to_midi('Bb-1'), 10.0)
        self.assertEqual(c.pitch_str_to_midi('A#-1'), 10.0)

    def test_handles_microtones(self):
        self.assertEqual(c.pitch_str_to_midi('B(2/3)b4'), 70.33)
        self.assertEqual(c.pitch_str_to_midi('F(1/2)#2'), 41.5)

class TestPitchObjToMidi(unittest.TestCase):
    def test_handles_chromatic_pitches(self):
        with mock.patch('hz_convert.converters.assign_diatonic_pc', \
                side_effect=[0, 11, 9, 5, 2, 4]), \
                mock.patch('hz_convert.converters.check_midi_range'):
            pitch_objs = [
                mock.Mock(diatonic_pc='C', accidental='', octave=4, cents_dev=0.0),
                mock.Mock(diatonic_pc='B', accidental='b', octave=3, cents_dev=0.0),
                mock.Mock(diatonic_pc='A', accidental='#', octave=3, cents_dev=0.0),
                mock.Mock(diatonic_pc='F', accidental='x', octave=-1, cents_dev=0.0),
                mock.Mock(diatonic_pc='D', accidental='', octave=7, cents_dev=0.0),
                mock.Mock(diatonic_pc='E', accidental='d', octave=5, cents_dev=0.0),
            ]
            self.assertListEqual([c.pitch_obj_to_midi(pitch) for pitch in pitch_objs], [60.0, 58.0, 58.0, 7.0, 98.0, 74.0])

    def test_handles_microtonal_pitches(self):
        with mock.patch('hz_convert.converters.check_midi_range'):
            pitch_objs = [
                mock.Mock(diatonic_pc='C', accidental='', octave=4, cents_dev=20.0),
                mock.Mock(diatonic_pc='B', accidental='b', octave=3, cents_dev=30.0),
                mock.Mock(diatonic_pc='A', accidental='#', octave=3, cents_dev_direction='-', cents_dev=-50.0),
                mock.Mock(diatonic_pc='F', accidental='x', octave=-1, cents_dev=-200.0),
                mock.Mock(diatonic_pc='D', accidental='', octave=7, cents_dev=-3.0),
                mock.Mock(diatonic_pc='E', accidental='d', octave=5, cents_dev=5.5)
            ]
            self.assertListEqual([c.pitch_obj_to_midi(pitch) for pitch in pitch_objs], [60.20, 58.30, 57.50, 5.00, 97.97, 74.06])

    def test_handles_out_of_range_pitches(self):
        with mock.patch('hz_convert.converters.check_midi_range'):
            pitch_objs = [
                mock.Mock(diatonic_pc='C', accidental='', octave=-2, cents_dev=0.0),
                mock.Mock(diatonic_pc='C', accidental='', octave=10, cents_dev=0.0),
            ]
            self.assertListEqual([c.pitch_obj_to_midi(pitch) for pitch in pitch_objs], [-12, 132])

class TestPitchStrToPitchObj(unittest.TestCase):
    def test_handles_good_chromatic_input(self):
        with mock.patch('hz_convert.converters.compute_cents_dev', side_effect = [
            ('', 0), ('', 0), ('', 0), ('', 0), ('', 0)
        ]):
            pitch_strs = ['Cn3', 'C3', 'Bb2', 'Ex-2', 'Gd200']
            expected_objs = [
                c.Pitch('C', 'n', 3, 0),
                c.Pitch('C', '', 3, 0),
                c.Pitch('B', 'b', 2, 0),
                c.Pitch('E', 'x', -2, 0),
                c.Pitch('G', 'd', 200, 0),
            ]
            computed_objs = [c.pitch_str_to_pitch_obj(pitch_str) for pitch_str in pitch_strs]
            comparison = [compare_pitch_objs(computed_obj, expected_obj) for computed_obj, expected_obj in zip(computed_objs, expected_objs)]

            self.assertListEqual(comparison, [True, True, True, True, True])

    def test_handles_good_microtone_input(self):
        with mock.patch('hz_convert.converters.compute_cents_dev', side_effect = [ \
            ('', 33.333), ('', -62.500), ('', 260.000) \
        ]):
            pitch_strs = ['C(1/3)#3', 'D(5/8)b-1', 'B(13/5)#-5']
            expected_objs = [
                c.Pitch('C', '', 3, 33.333),
                c.Pitch('D', '', -1, -62.500),
                c.Pitch('B', '', -5, 260.000),
            ]
            computed_objs = [c.pitch_str_to_pitch_obj(pitch_str) for pitch_str in pitch_strs]
            comparison = [compare_pitch_objs(computed_obj, expected_obj) for computed_obj, expected_obj in zip(computed_objs, expected_objs)]

            self.assertListEqual(comparison, [True, True, True])

    def test_handles_broken_input(self):
        with self.assertRaisesRegex(ValueError, '^Invalid pitch'):
            c.pitch_str_to_pitch_obj('C')

        with self.assertRaisesRegex(ValueError, '^Invalid pitch'):
            c.pitch_str_to_pitch_obj('5')

        with self.assertRaisesRegex(ValueError, '^Invalid pitch'):
            c.pitch_str_to_pitch_obj('C(1/3)5')

        with self.assertRaisesRegex(ValueError, '^Invalid pitch'):
            c.pitch_str_to_pitch_obj('D(1/3)#')

        with self.assertRaisesRegex(ValueError, '^Invalid pitch'):
            c.pitch_str_to_pitch_obj('C#(1/3)5')

        with self.assertRaisesRegex(ValueError, '^Invalid pitch'):
            c.pitch_str_to_pitch_obj('C(1/35#')

        with self.assertRaisesRegex(ValueError, '^Invalid pitch'):
            c.pitch_str_to_pitch_obj('C(/3)#5')

class TestMidiHzConversions(unittest.TestCase):
    def test_midi_to_hz_standard_tuning(self):
        self.assertEqual(c.midi_to_hz(69, STD_A4), 440.0)
        self.assertEqual(c.midi_to_hz(60, STD_A4), 261.626)
        self.assertEqual(c.midi_to_hz(78.43, STD_A4), 758.599)

    def test_midi_to_hz_custom_tuning(self):
        self.assertEqual(c.midi_to_hz(69, NEW_A4), 423.519)
        self.assertEqual(c.midi_to_hz(60, NEW_A4), 251.826)
        self.assertEqual(c.midi_to_hz(78.43, NEW_A4), 730.184)

    def test_hz_to_midi_standard_tuning(self):
        with mock.patch('hz_convert.converters.check_midi_range'):
            self.assertEqual(c.hz_to_midi(440.0, STD_A4), 69.0)
            self.assertEqual(c.hz_to_midi(261.626, STD_A4), 60.0)
            self.assertEqual(c.hz_to_midi(758.599, STD_A4), 78.43)

    def test_hz_to_midi_custom_tuning(self):
        with mock.patch('hz_convert.converters.check_midi_range'):
            self.assertEqual(c.hz_to_midi(423.519, NEW_A4), 69.0)
            self.assertEqual(c.hz_to_midi(251.826, NEW_A4), 60.0)
            self.assertEqual(c.hz_to_midi(730.184, NEW_A4), 78.43)

class TestMidiToPitchLoop(unittest.TestCase):
    def test_exits_normally(self):
        with mock.patch('builtins.input', side_effect=['X']), \
                mock.patch('sys.stdout'):
            self.assertTrue(c.midi_to_pitch_loop(STD_A4))

    def test_good_input_standard_a4(self):
        with mock.patch('builtins.input', side_effect=['69', '60 22.5', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(STD_A4))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertTrue('- Pitch name: A4 (+0.0 c)' in out)
            self.assertTrue('- Hz value: 440.00' in out)
            self.assertTrue('- Pitch names: C4 (+0.0 c), Bb0 (+50.0 c)' in out)
            self.assertTrue('- Hz values: 261.63, 29.99' in out)

    def test_good_input_new_a4(self):
        with mock.patch('builtins.input', side_effect=['69', '60 22.5', 'X']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(NEW_A4))
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line[0] == '-']
            self.assertTrue('- Pitch name: A4 (+0.0 c)' in out)
            self.assertTrue('- Hz value: 423.52' in out)
            self.assertTrue('- Pitch names: C4 (+0.0 c), Bb0 (+50.0 c)' in out)
            self.assertTrue('- Hz values: 251.83, 28.87' in out)

    def test_broken_input(self):
        with mock.patch('builtins.input', side_effect=['not a number', 'x']), \
                mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            self.assertTrue(c.midi_to_pitch_loop(STD_A4))
            out = mock_stdout.getvalue().strip().split('\n')[-1]
            self.assertEqual(out, '[error] Syntax error: Not a numerical input.')

class TestMidiToPitch(unittest.TestCase):
    def test_good_input(self):
        with mock.patch('hz_convert.converters.assign_name', side_effect=[('A', ''), ('D', '#')]), \
                mock.patch('hz_convert.converters.get_cents_dev', side_effect=[23.2, -43.1]), \
                mock.patch('hz_convert.converters.get_octave', side_effect=[3, 5]):

            pitch1 = c.midi_to_pitch(57.232)
            pitch2 = c.midi_to_pitch(75.569)

            self.assertListEqual([
                pitch1.diatonic_pc,
                pitch1.accidental,
                pitch1.octave,
                pitch1.cents_dev
            ], ['A', '', 3, 23.2])

            self.assertListEqual([
                pitch2.diatonic_pc,
                pitch2.accidental,
                pitch2.octave,
                pitch2.cents_dev
            ], ['D', '#', 5, -43.1])

class TestOutputs(unittest.TestCase):
    def test_hz_string_one_good_input(self):
        self.assertEqual(c.hz_string(440.0), '- Hz value: 440.00')
        self.assertEqual(c.hz_string(261.626), '- Hz value: 261.63')
        self.assertEqual(c.hz_string(730.184), '- Hz value: 730.18')

    def test_hz_string_many_good_inputs(self):
        self.assertEqual(c.hz_string([440, 323.4445, 289.2]), '- Hz values: 440.00, 323.44, 289.20')

    def test_hz_string_bad_input(self):
        with self.assertRaisesRegex(TypeError, 'Hz values must be floats.'):
            c.hz_string([240.5, 'invalid Hz value'])

    def test_pitch_string_good_input(self):
        pitches = [
            c.Pitch('A', '', 3, 23.2),
            c.Pitch('D', '#', 5, -43.1)
        ]

        self.assertEqual(c.pitch_string(pitches[0]), '- Pitch name: A3 (+23.2 c)')
        self.assertEqual(c.pitch_string(pitches[1]), '- Pitch name: D#5 (-43.1 c)')

    def test_midi_string_one_good_input(self):
        self.assertEqual(c.midi_string(60.20, microtonal = False), '- MIDI value: 60')
        self.assertEqual(c.midi_string(52.00, microtonal = True), '- MIDI value: 52.00')

    def test_midi_string_many_good_inputs(self):
        self.assertEqual(c.midi_string([60.20, 43.9, 15], microtonal = False), '- MIDI values: 60, 43, 15')
        self.assertEqual(c.midi_string([60.20, 43.9, 15], microtonal = True), '- MIDI values: 60.20, 43.90, 15.00')

    def test_midi_string_broken_input(self):
        with self.assertRaisesRegex(TypeError, 'MIDI values must be numerical'):
            c.midi_string([34, 'invalid value'])

class TestPitchToMidiHelpers(unittest.TestCase):
    def test_compute_cents_dev_good_input(self):
        self.assertEqual(c.compute_cents_dev('b', None, None), ('b', 0))
        self.assertEqual(c.compute_cents_dev('b', '3', '4'), ('', -75.000))
        self.assertEqual(c.compute_cents_dev('#', '1', '4'), ('', 25.000))

    def test_compute_cents_dev_restricts_accidentals(self):
        with self.assertRaisesRegex(ValueError, 'Only # and b are allowed with microtone \(fraction\) notation.'):
            c.compute_cents_dev('n', '3', '4')

    def test_compute_cents_dev_requires_number_strings(self):
        with self.assertRaisesRegex(ValueError, 'Numerator or denominator not a number.'):
            c.compute_cents_dev('b', '3', 'invalid')

    def test_accidental_to_cents_dev_good_input(self):
        self.assertEqual(c.accidental_to_cents_dev(None), 0)
        self.assertEqual(c.accidental_to_cents_dev('n'), 0)
        self.assertEqual(c.accidental_to_cents_dev('x'), 200)
        self.assertEqual(c.accidental_to_cents_dev('d'), -200)
        self.assertEqual(c.accidental_to_cents_dev('#'), 100)
        self.assertEqual(c.accidental_to_cents_dev('b'), -100)

    def test_accidental_to_cents_dev_broken_input(self):
        with self.assertRaisesRegex(KeyError, 'Invalid accidental type.'):
            c.accidental_to_cents_dev('y')

class TestMidiToPitchHelpers(unittest.TestCase):
    def test_assign_name_good_input(self):
        self.assertTupleEqual(c.assign_name(0), ('C', ''))
        self.assertTupleEqual(c.assign_name(8), ('G', '#'))
        self.assertTupleEqual(c.assign_name(10), ('B', 'b'))

    def test_assign_name_fails_out_of_range(self):
        with self.assertRaisesRegex(KeyError, 'Invalid pitch class number.'):
            c.assign_name(12)

    def test_assign_diatonic_pc_good_input(self):
        self.assertEqual(c.assign_diatonic_pc('F'), 5)
        self.assertEqual(c.assign_diatonic_pc('B'), 11)

    def test_assign_diatonic_pc_broken_input(self):
        with self.assertRaisesRegex(KeyError, 'Invalid pitch class name.'):
            c.assign_diatonic_pc('invalid name')

        with self.assertRaisesRegex(KeyError, 'Invalid pitch class name.'):
            c.assign_diatonic_pc(8)

    def test_check_midi_range(self):
        with mock.patch('sys.stdout', new = StringIO()) as mock_stdout:
            c.check_midi_range(-1)
            c.check_midi_range(128)
            out = mock_stdout.getvalue().strip().split('\n')[-2:]
            warning = '[warning] MIDI note outside of the defined range 0-127.'
            self.assertListEqual(out, [warning, warning])

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
        self.assertEqual(c.get_cents_dev(120.4, 120), 40.0)
        self.assertEqual(c.get_cents_dev(120.4, 121), -60.0)

    def test_get_cents_dev_returns_decimals(self):
        self.assertEqual(c.get_cents_dev(120.423, 121), -57.7)

        # Should round answer to 1 decimal place
        self.assertEqual(c.get_cents_dev(120.4232, 121), -57.7)




if __name__ == '__main__':
    unittest.main()

