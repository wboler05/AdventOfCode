#!/usr/bin/env python3

import argparse, sys, os
import numpy as np

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("input_file", help="Input file of inputs")
  parser.add_argument("expected_sum", type=int, help="Expected sum of two numbers")
  args = parser.parse_args()

  assert(os.path.exists(args.input_file))

  data = None
  with open(args.input_file, 'r') as ifile:
    data = np.array(ifile.read().split('\n'))
    data = data[:-1].astype(int)

  for i in range(len(data)):
    for j in range(i+1, len(data)):
      a = data[i]
      b = data[j]
      if a + b == args.expected_sum:
        print("Numbers: {}, {}\nMultiplied: {}".format(a,b,a*b))


