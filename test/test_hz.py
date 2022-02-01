import unittest

from hz_convert import converters

class TestMidiToPitch(unittest.TestCase):
    def test_assign_name_to_Cn(self):
        self.assertEqual(converters.assign_name(0), 'Cn')
        self.assertEqual(converters.assign_name(8), 'G#')
        self.assertEqual(converters.assign_name(10), 'Bb')

    def test_assign_name_fails_out_of_range(self):
        with self.assertRaises(KeyError):
            converters.assign_name(12)


if __name__ == '__main__':
    unittest.main()
