#!/usr/bin/env python3

import argparse, os, sys
import re

def execute(operations):
  instruction_counts = [0]*len(operations)
  accumulator = 0
  idx = 0
  while(True):
    opcode, operand = operations[idx]
    print("Acc({}),\tIdx({}),\t - Opcode({}),\tOperand({})".format(
      accumulator, idx, opcode, operand
    ))
    instruction_counts[idx] += 1
    if instruction_counts[idx] == 2:
      break
    if opcode == 'acc':
      accumulator += operand
      idx += 1
    elif opcode == 'nop':
      idx += 1
    elif opcode == 'jmp':
      idx += operand

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  args = parser.parse_args()
  
  assert(os.path.exists(args.input_filename))

  line_pattern = "^(?P<opcode>[\w]+) ?(?P<operand>[0-9\-+]+)?$"
  data = None
  with open(args.input_filename, 'r') as ifile:
    data = ifile.read().split('\n')

  operations = list()
  for d in data:
    m = re.search(line_pattern, d)
    if m is not None:
      operations.append((m.group('opcode'), int(m.group('operand'))))

  #for o in operations:
  #  print(o)
  execute(operations)

if __name__ == '__main__':
  main()

