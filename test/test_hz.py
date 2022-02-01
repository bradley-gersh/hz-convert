import unittest

from hz_convert import converters

class TestMidiToPitch(unittest.TestCase):
    def test_assign_name(self):
        self.assertEqual(converters.assign_name(0), 'Cn')

if __name__ == '__main__':
    unittest.main()
