#!/usr/bin/env python3

import argparse, os, sys
import re

def load_operations(input_filename):
  assert(os.path.exists(input_filename))

  line_pattern = "^(?P<opcode>[\w]+) ?(?P<operand>[0-9\-+]+)?$"
  data = None
  with open(input_filename, 'r') as ifile:
    data = ifile.read().split('\n')

  operations = list()
  for d in data:
    m = re.search(line_pattern, d)
    if m is not None:
      operations.append([m.group('opcode'), int(m.group('operand'))])
  return operations
  

def execute(operations, verbose=False):
  instruction_counts = [0]*len(operations)
  accumulator = 0
  idx = 0
  valid = True
  while(True):
    if idx >= len(operations):
      break
    opcode, operand = operations[idx]
    if verbose:
      print("Acc({}),\tIdx({}),\t - Opcode({}),\tOperand({})".format(
        accumulator, idx, opcode, operand
      ))
    instruction_counts[idx] += 1
    if instruction_counts[idx] == 2:
      valid = False
      break
    if opcode == 'acc':
      accumulator += operand
      idx += 1
    elif opcode == 'nop':
      idx += 1
    elif opcode == 'jmp':
      idx += operand
  return accumulator, valid

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  args = parser.parse_args()
  
  operations = load_operations(args.input_filename)
  acc, valid = execute(operations)
  print("Final ACC: {}, \tValid: {}".format(acc, valid))

if __name__ == '__main__':
  main()

