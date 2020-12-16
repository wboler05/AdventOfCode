#!/usr/bin/env python3

'''
Reason for brute-force: 
  NOP are supposed to have 0, but I'm not sure if that's a valid check
  for a switch.  Therefore, I'd rather just switch each until it terminates.
  O(N^2), but oh well. 
'''

import argparse, os, sys
from part1 import load_operations, execute
from copy import deepcopy

def fix_mutation(operations, verbose=False):
  test_set = set()
  for i,o in enumerate(operations):
    if o[0] == 'jmp' or o[0] == 'nop':
      test_set.add(i)
  while(True):
    cache = deepcopy(operations)
    if len(test_set) == 0:
      break
    idx = test_set.pop()
    if cache[idx][0] == 'nop':
      cache[idx][0] = 'jmp'
    elif cache[idx][0] == 'jmp':
      cache[idx][0] = 'nop'
    acc, valid = execute(cache)
    if valid:
      return acc

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('input_filename', type=str)
  parser.add_argument("--verbose", "-v", action='store_true')
  args = parser.parse_args()

  operations = load_operations(args.input_filename)
  acc = fix_mutation(operations, args.verbose)
  print("Final ACC: {}".format(acc))
