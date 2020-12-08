#!/usr/bin/env python3

import argparse, os, sys
from part1 import extract_color_rules


def count_children(bag_dict, child_color):

  child_count = 1
  if child_color in bag_dict:
    for v in bag_dict[child_color]:
      gc_color = v['bag_color']
      bag_count = v['bag_count']
      child_count += count_children(bag_dict, gc_color) * bag_count
  return child_count


def count_inner_bags(bag_dict, my_color):
  '''
  I had to make two functions because I'm an idiot
  '''

  color_count = 0
  if my_color in bag_dict:
    for v in bag_dict[my_color]:
      child_color = v['bag_color']
      bag_count = v['bag_count']
      color_count += count_children(bag_dict, child_color) * bag_count
  return color_count


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  parser.add_argument("color", type=str)
  args = parser.parse_args()

  assert(os.path.exists(args.input_filename))

  data = None
  with open(args.input_filename, 'r') as ifile:
    data = ifile.read().split('\n')

  bag_color_rules_dict, inner_to_outer_dict = extract_color_rules(data)
  inner_bag_count = count_inner_bags(bag_color_rules_dict, args.color)
  print("Inner Bag Count: {}".format(inner_bag_count))

if __name__ == '__main__':
  main()
