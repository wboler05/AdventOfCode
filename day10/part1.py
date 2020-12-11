#!/usr/bin/env python

import argparse, os, sys
import numpy as np

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  parser.add_argument("--starting-port", "-s", type=int, default=0)
  args = parser.parse_args()
  
  assert(os.path.exists(args.input_filename))

  data = None
  with open(args.input_filename, 'r') as ifile:
    data = np.array([r for r in ifile.read().split('\n') if len(r) > 0]).astype(int)
  data = sorted(data)

  builtin_device_joltage = np.max(data) + 3
  potential = args.starting_port
  failed_idx = None
  diff_dict = dict()
  for i,d in enumerate(data):
    diff = d - potential
    if diff > 3 or diff <= 0:
      failed_idx = i
      break
    potential = d
    if diff not in diff_dict:
      diff_dict[diff] = 0
    diff_dict[diff] += 1

  if failed_idx is not None:
    print("Failed at idx({}): {}".format(idx, data[idx]))
    return
  
  final_diff = builtin_device_joltage - potential
  if final_diff > 3 or final_diff <= 0:
    print("Failed to get the right voltage: Potential({}), BuiltIn({})".format(potential, builtin_device_joltage))
    return
  if final_diff not in diff_dict:
    diff_dict[final_diff] = 1
  else:
    diff_dict[final_diff] += 1

  print("Differences: {}".format(diff_dict))

  mult = 0
  if 1 in diff_dict and 3 in diff_dict:
    mult = diff_dict[1] * diff_dict[3]
  
  print("Multiply diff[1] x diff[3] = {}".format(mult))
  
if __name__ == '__main__':
  main()
