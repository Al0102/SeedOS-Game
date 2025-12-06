from unittest import TestCase

from game.utilities import sum_vectors


class TestSumVectors(TestCase):
    def test_sum_2_by_2_0_0(self):
        vectors = [(0, 0) for _ in range(2)]
        expected = (0, 0)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_2_0_0(self):
        vectors = [(0, 0, 0) for _ in range(2)]
        expected = (0, 0, 0)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_2_by_3_value_0(self):
        vectors = [(0, 0) for _ in range(3)]
        expected = (0, 0)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_3_value_0(self):
        vectors = [(0, 0, 0) for _ in range(3)]
        expected = (0, 0, 0)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_2_by_2_values_positive(self):
        vectors = (
            (5, 6),
            (3, 4))
        expected = (8, 10)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_2_by_2_values_negative(self):
        vectors = (
            (-5, -6),
            (-3, -4))
        expected = (-8, -10)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_2_by_2_values_mixed(self):
        vectors = (
            (-5, 6),
            (3, 4))
        expected = (-2, 10)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_2_values_positive(self):
        vectors = (
            (5, 6, 7),
            (3, 4, 6))
        expected = (8, 10, 13)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_2_values_negative(self):
        vectors = (
            (-5, -6, -7),
            (-3, -4, -6))
        expected = (-8, -10, -13)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_2_values_mixed(self):
        vectors = (
            (-5, 6, 7),
            (3, 4, -6))
        expected = (-2, 10, 1)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_3_values_positive(self):
        vectors = (
            (5, 6, 7),
            (3, 4, 6),
            (10, 22, 9))
        expected = (18, 32, 22)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_3_values_negative(self):
        vectors = (
            (-5, -6, -7),
            (-3, -4, -6),
            (-10, -22, -9))
        expected = (-18, -32, 22)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)

    def test_sum_3_by_3_values_mixed(self):
        vectors = (
            (-5, -6, 7),
            (-3, 0, -6),
            (10, -22, -1))
        expected = (2, -28, 0)
        actual = sum_vectors(*vectors)
        self.assertEqual(expected, actual)
