#!/usr/bin/env python

import unittest

from part1 import get_2020th_number, get_nth_number

class TestDay15(unittest.TestCase):

  def test_0_3_6(self):
    num = get_nth_number([0, 3, 6], 10)
    self.assertEqual(num, 0)
  def test_1_3_2(self):
    num = get_2020th_number([1, 3, 2])
    self.assertEqual(num, 1)

  def test_2_1_3(self):
    num = get_2020th_number([2, 1, 3])
    self.assertEqual(num, 10)

  def test_1_2_3(self):
    num = get_2020th_number([1, 2, 3])
    self.assertEqual(num, 27)

  def test_2_3_1(self):
    num = get_2020th_number([2, 3, 1])
    self.assertEqual(num, 78)

  def test_3_2_1(self):
    num = get_2020th_number([3, 2, 1])
    self.assertEqual(num, 438)

  def test_3_1_2(self):
    num = get_2020th_number([3, 1, 2])
    self.assertEqual(num, 1836)
