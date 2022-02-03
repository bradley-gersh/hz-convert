import unittest
from unittest import mock
from io import StringIO

import hz_convert.start as s

class TestMainMenu(unittest.TestCase):
    def test_handles_default_a4(self):
        with mock.patch('hz_convert.start.set_a4', return_value = 440.0) as mock_seta4, \
                mock.patch('hz_convert.start.top_menu') as mock_topmenu, \
                mock.patch('sys.stdout') as mock_stdout:
            s.main()
            mock_seta4.assert_called_once()
            mock_topmenu.assert_called_once_with(440.0)

    def test_eof_exits(self):
        with self.assertRaises(SystemExit), \
            mock.patch('hz_convert.start.set_a4', side_effect = EOFError), \
                mock.patch('sys.stdout') as mock_stdout:
            s.main()

class TestSetA4(unittest.TestCase):
    def test_sets_a4(self):
        with mock.patch('builtins.input', side_effect = ['230']), \
                mock.patch('hz_convert.start.top_menu') as mock_topmenu:
            self.assertEqual(s.set_a4(), 230.0)

    def test_handles_broken_input(self):
        with mock.patch('builtins.input', side_effect = ['sdf']), \
                mock.patch('sys.stdout') as mock_stdout, \
                mock.patch('hz_convert.start.top_menu') as mock_topmenu:
            self.assertEqual(s.set_a4(), 440.0)

    def test_handles_empty_input(self):
        with mock.patch('builtins.input', side_effect = ['']), \
                mock.patch('hz_convert.start.top_menu') as mock_topmenu:
            self.assertEqual(s.set_a4(), 440.0)


class TestTopMenu(unittest.TestCase):
    def test_exits_normally(self):
        with mock.patch('builtins.input', side_effect = ['x']), \
                mock.patch('sys.stdout') as mock_stdout:
            self.assertTrue(s.top_menu(440.0))

    def test_calls_loop_1(self):
        with mock.patch('builtins.input', side_effect = ['1', 'x']), \
                mock.patch('hz_convert.converters.pitch_to_hz_loop') as mock_loop, \
                mock.patch('sys.stdout') as mock_stdout:
            s.top_menu(440.0)
            mock_loop.assert_called_once_with(440.0)

    def test_calls_loop_2(self):
        with mock.patch('builtins.input', side_effect = ['2', 'x']), \
                mock.patch('hz_convert.converters.hz_to_pitch_loop') as mock_loop, \
                mock.patch('sys.stdout') as mock_stdout:
            s.top_menu(440.0)
            mock_loop.assert_called_once_with(440.0)

    def test_calls_loop_3(self):
        with mock.patch('builtins.input', side_effect = ['3', 'x']), \
                mock.patch('hz_convert.converters.midi_to_pitch_loop') as mock_loop, \
                mock.patch('sys.stdout') as mock_stdout:
            s.top_menu(440.0)
            mock_loop.assert_called_once_with(440.0)

    def test_invalid_input(self):
        with mock.patch('builtins.input', side_effect = ['test', 'x']), \
                mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            s.top_menu(440.0)
            out = mock_stdout.getvalue().strip().split('\n')
            out = [line for line in out if len(line) > 0 and line == 'Make a selection:']
            self.assertEqual(len(out), 2)
