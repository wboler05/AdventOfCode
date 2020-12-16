#!/usr/bin/env python

import unittest

from part1 import get_nth_number

class TestDay15(unittest.TestCase):

  def test_0_3_6(self):
    num = get_nth_number([0, 3, 6], 30000000)
    self.assertEqual(num, 175594)

  def test_1_3_2(self):
    num = get_nth_number([1, 3, 2], 30000000)
    self.assertEqual(num, 2578)

  def test_2_1_3(self):
    num = get_nth_number([2, 1, 3], 30000000)
    self.assertEqual(num, 3544142)

  def test_1_2_3(self):
    num = get_nth_number([1, 2, 3], 30000000)
    self.assertEqual(num, 261214)

  def test_2_3_1(self):
    num = get_nth_number([2, 3, 1], 30000000)
    self.assertEqual(num, 6895259)

  def test_3_2_1(self):
    num = get_nth_number([3, 2, 1], 30000000)
    self.assertEqual(num, 18)

  def test_3_1_2(self):
    num = get_nth_number([3, 1, 2], 30000000)
    self.assertEqual(num, 362)
