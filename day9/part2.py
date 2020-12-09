#!/usr/bin/env python3

import argparse, os, sys
import numpy as np

from part1 import find_invalid_number, load_data

def find_encryption_weakness(input_filename, preamble_size):
  fail_number = find_invalid_number(input_filename, preamble_size)
  if fail_number is not None:
    data = load_data(input_filename)
    for i in range(len(data)):
      for j in range(i+1, len(data)+1):
        snip = data[i:j]
        if np.sum(snip) == fail_number:
          return np.min(snip) + np.max(snip)

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  parser.add_argument("--preamble", "-p", type=int, default=25)
  args = parser.parse_args()
  
  encryption_weakness = find_encryption_weakness(args.input_filename, args.preamble)
  print("Encryption Weakness: {}".format(encryption_weakness))
  
if __name__ == '__main__':
  main()
        
