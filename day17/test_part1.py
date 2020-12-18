import unittest
import numpy as np
from numpy.testing import assert_array_equal

class TestPart1(unittest.TestCase):
    def test_load_data(self):
        from part1 import load_data
        initial_state = np.array([
            ['.', '#', '.'],
            ['.', '.', '#'],
            ['#', '#', '#']

        ])
        data = load_data('example1.txt')
        self.assertIsNone(
            assert_array_equal(
                initial_state,
                data
            )
        )

