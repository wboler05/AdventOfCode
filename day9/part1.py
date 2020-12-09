#!/usr/bin/env python3

import argparse, os, sys
import numpy as np

def load_data(input_filename):
  assert(os.path.exists(input_filename))
  data = None
  with open(input_filename, 'r') as ifile:
    data = ifile.read().split('\n')

  comms = list()
  for d in data:
    if len(d) > 0:
      comms.append(d)
  comms = np.array(comms).astype('uint64')
  return comms

def find_invalid_number(input_filename, preamble_size):
  
  assert(preamble_size > 0)
  comms = load_data(input_filename)

  fail_number = None
  for i in range(preamble_size+1, len(comms)):
    preamble = comms[i-preamble_size-1:i-1]
    eval_number = comms[i-1]
    print(preamble, eval_number)
    found = False
    for j in range(len(preamble)):
      for k in range(j+1, len(preamble)):
        if preamble[j] + preamble[k] == eval_number:
          found = True
          break
    if not found:
      fail_number = eval_number
      break

  return fail_number


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  parser.add_argument("--preamble", "-p", type=int, default=25)
  args = parser.parse_args()

  fail_number = find_invalid_number(args.input_filename, args.preamble)
  print("Failure at: {}".format(fail_number))


if __name__ == '__main__':
  main()
