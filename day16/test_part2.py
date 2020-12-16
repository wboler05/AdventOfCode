import unittest

from part1 import load_data, validate_tickets
from part2 import determine_column_rules

class TestPart2(unittest.TestCase):
    def test_determine_coumn_rules(self):
        data = load_data('example.txt')
        valid_tickets, error_rate = validate_tickets(data)
        column_rules = determine_column_rules(data, valid_tickets)
        
        self.assertEqual(column_rules[0], 'row')
        self.assertEqual(column_rules[1], 'class')
        self.assertEqual(column_rules[2], 'seat')