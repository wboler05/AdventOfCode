import unittest
from part1 import load_data
import numpy as np
from numpy.testing import assert_array_equal

class TestPart1(unittest.TestCase):
    def test_load_data(self):
        data = load_data('example.txt')
        self.assertIn('rules', data)
        self.assertIn('your_ticket', data)
        self.assertIn('nearby_tickets', data)

        self.assertIn('class', data['rules'])
        self.assertIn('row', data['rules'])
        self.assertIn('seat', data['rules'])

        self.assertIsNone(assert_array_equal((1, 3), data['rules']['class'][0]))
        self.assertIsNone(assert_array_equal((5, 7), data['rules']['class'][1]))

        self.assertIsNone(assert_array_equal((6, 11), data['rules']['row'][0]))
        self.assertIsNone(assert_array_equal((33, 44), data['rules']['row'][1]))

        self.assertIsNone(assert_array_equal((13, 40), data['rules']['seat'][0]))
        self.assertIsNone(assert_array_equal((45, 50), data['rules']['seat'][1]))

        self.assertIsNone(assert_array_equal([7, 1, 14], data['your_ticket']))

        self.assertIsNone(assert_array_equal([7, 3, 47], data['nearby_tickets'][0]))
        self.assertIsNone(assert_array_equal([40, 4, 50], data['nearby_tickets'][1]))
        self.assertIsNone(assert_array_equal([55, 2, 20], data['nearby_tickets'][2]))
        self.assertIsNone(assert_array_equal([38, 6, 12], data['nearby_tickets'][3]))

    def test_example(self):
        from part1 import validate_tickets
        data = load_data('example.txt')
        valid_tickets, error_rate = validate_tickets(data)
        self.assertEqual(error_rate, 71)
