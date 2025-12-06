from unittest import TestCase
from unittest.mock import patch

from game.terminal.screen import point_within_screen


class TestPointWithinScreen(TestCase):
    @patch("game.terminal.screen.get_screen_size", side_effect=[(1, 1)])
    def test_point_0_0_screen_smallest(self, _):
        point = (0, 0)
        expected = (False, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_0_0_screen_large_equal(self, _):
        point = (0, 0)
        expected = (False, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(20, 10)])
    def test_point_0_0_screen_large_unequal(self, _):
        point = (0, 0)
        expected = (False, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(1, 1)])
    def test_point_1_0_screen_smallest(self, _):
        point = (1, 0)
        expected = (True, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(1, 1)])
    def test_point_0_1_screen_smallest(self, _):
        point = (0, 1)
        expected = (False, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(1, 1)])
    def test_point_1_1_screen_smallest(self, _):
        point = (1, 1)
        expected = (True, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_1_0_screen_large_equal(self, _):
        point = (1, 0)
        expected = (True, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_0_1_screen_large_equal(self, _):
        point = (0, 1)
        expected = (False, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_1_1_screen_large_equal(self, _):
        point = (1, 1)
        expected = (True, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_1_0_screen_large_unequal(self, _):
        point = (1, 0)
        expected = (True, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_0_1_screen_large_unequal(self, _):
        point = (0, 1)
        expected = (False, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_1_1_screen_large_unequal(self, _):
        point = (1, 1)
        expected = (True, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_10_10_screen_large_equal(self, _):
        point = (10, 10)
        expected = (True, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(10, 10)])
    def test_point_10_11_screen_large_equal(self, _):
        point = (10, 11)
        expected = (True, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(20, 10)])
    def test_point_20_10_screen_large_equal(self, _):
        point = (20, 10)
        expected = (True, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(20, 10)])
    def test_point_20_11_screen_large_unequal(self, _):
        point = (20, 11)
        expected = (True, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(20, 10)])
    def test_point_21_10_screen_large_unequal(self, _):
        point = (21, 10)
        expected = (False, True)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)

    @patch("game.terminal.screen.get_screen_size", side_effect=[(20, 10)])
    def test_point_21_11_screen_large_unequal(self, _):
        point = (21, 11)
        expected = (False, False)
        actual = point_within_screen(point)
        self.assertEqual(expected, actual)
