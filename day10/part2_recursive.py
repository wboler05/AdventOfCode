#!/usr/bin/env python3

'''
Recursive Divide and Conquer - works faster than bruteforce
Takes a bunch of memory (maxes my 32GB)
Death of a system can incur
Have a swapfile...
'''

import argparse, os, sys
import numpy as np
from part2 import HashSet, validate, load_data

import tqdm

sweep_depth = 20

def sweep(data, left_val=None, right_val=None):
  print(data)
  found_set = HashSet()
  if not validate(data):
    #print("Not valid: {}".format(data))
    return
    
  search_set = HashSet()
  search_set.add(data)
  while not search_set.empty():
    search_list = search_set.pop()
    if search_list in found_set:
      continue
    else:
      found_set.add(search_list)
      for i in range(0, len(search_list)):
        check = np.delete(search_list, i)
        if check not in found_set:
          if validate(check, left_val, right_val):
            #print("Valid Arr: {}".format(check))
            search_set.add(check)
  return found_set


def search_valid(data, left_val=None, right_val=None):
  global sweep_depth
  print(data)

  if len(data) <= sweep_depth:
    return sweep(data, left_val, right_val)
  else:
    m = int(len(data) / 2)
    print(" - Left Search")
    left_set = search_valid(data[:m], left_val, None)
    print(" - Right Search")
    right_set = search_valid(data[m:], None, right_val)
    #print(" - m({}):\t{}, {}".format(m,len(left_set), len(right_set)))
    print('{} to {}'.format(data[0], data[-1]))
    found_set = HashSet()
    print("Check left to right")
    total = len(left_set) * len(right_set)
    p = tqdm.tqdm(total=total)
    for left in left_set:
      if len(left) == 0:
        p.update(len(right_set))
        continue
      for right in right_set:
        p.update(1)
        if len(right) == 0:
          continue
        diff = right[0] - left[-1]
        if diff <= 3 and diff > 0:
          arr = np.hstack((left, right))
          found_set.add(arr)
    p.close()
    print("Complete {} to {}".format(data[0], data[-1]))
    del left_set
    del right_set
    return found_set

def count_correct(found_set, first_element, final_element):
  i = 0
  for f in tqdm.tqdm(found_set):
    if f[0] == first_element and f[-1] == final_element:
      i += 1
  return i


def main():
  global sweep_depth

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  parser.add_argument("--sweep-depth", "-d", type=int, default=sweep_depth)
  args = parser.parse_args()
  assert(args.sweep_depth >= 5)
  sweep_depth = args.sweep_depth
  
  data = load_data(args.input_filename)
  
  found_set = search_valid(data)
  print("Correcting found set")
  #for s in found_set:
  #  print(" :: {}".format(s))
  valid_count = count_correct(found_set, data[0], data[-1])
  #for s in found_set:
  #  print(" - {}".format(s))
  print("Valid Count: {}".format(valid_count))

if __name__ == '__main__':
  main()
