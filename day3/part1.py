#!/usr/bin/env python3

import argparse, os, sys
import numpy as np

def count_trees(input_filename, right_steps, down_steps):

  assert(os.path.exists(input_filename))
  data = None
  with open(input_filename, 'r') as ifile:
    data = np.array(ifile.read().split('\n'))[:-1]

  new_data = list()
  for d in data:
    if len(d) > 1:
      new_data.append(np.array(list(d)))
  data = np.array(new_data)

  M,N = data.shape
  tree_count = 0
  x,y = 0,0
  right,down = 0,0
  while(y < M):

    char = data[y,x%N]
    if char == "#":
      tree_count += 1
    x += right_steps
    y += down_steps

  return tree_count 

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument('input_filename', type=str, help="Input File of trees")
  parser.add_argument('right_steps', type=int, help="Movement right count")
  parser.add_argument('down_steps', type=int, help="Movement down count")
  args = parser.parse_args()

  tree_count = count_trees(args.input_filename, args.right_steps, args.down_steps)
  print("Tree Count: {}".format(tree_count))
