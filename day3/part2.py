#!/usr/bin/env python3

import argparse, os, sys
from part1 import count_trees

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('input_filename', type=str, help="Input Filename")
  parser.add_argument('patterns', type=int, nargs="+", help="List of patterns (right, down) list")
  args = parser.parse_args()

  assert(os.path.exists(args.input_filename))
  assert(len(args.patterns) % 2 == 0)

  step_patterns = list()
  for i in range(0, len(args.patterns), 2):
    right_step = args.patterns[i]
    down_step = args.patterns[i+1]
    step_patterns.append((right_step, down_step))

  tree_counts = list()
  for p in step_patterns:
    tree_count = count_trees(args.input_filename, p[0], p[1])
    print("Tree Count(Right {}, Down {}): {}".format(p[0], p[1], tree_count))
    tree_counts.append(tree_count)

  m = 1
  for t in tree_counts:
    m *= t
  print("Multiplier: {}".format(m))

if __name__ == '__main__':
  main()
