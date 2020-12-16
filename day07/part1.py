#!/usr/bin/env python3

import argparse, os, sys
import re

def extract_color_rules(rule_list):

  # Return object
  bag_color_rules_dict = dict()
  inner_to_outer_dict = dict()

  # regex patterns
  first_pattern = "^(?:\s*)(?P<outer_bag_color>[\w ]+) bag(?:s?) contain (?P<bag_rule_list>[\d\w, ]+) bag(?:s?).$"
  second_pattern = "^(?:[\s]*)(?P<inner_bag_rule>[\w\d ]+)$"
  third_pattern = "^(?:\s*)(?P<bag_count>[\d]*) (?P<inner_bag_color>[\w]+ [\w]+)(?:\s?)(?: bags?)?$"
  
  # For each raw rule in the list
  for r in rule_list:
    # Extract the outer bag color and the inner bag rules
    m = re.search(first_pattern, r)
    if m is not None:
      #print(m.groups())
      outer_bag_color = m.group('outer_bag_color')
      #print(" - Outer Bag Color: {}".format(outer_bag_color))
      
      # Rules are keyed by outer_bag_color and appended to list
      bag_color_rules_dict[outer_bag_color] = list()
      
      # For each rule in the list (separated by commas)
      for g in m.group('bag_rule_list').split(','):
        # Extract a set of words and an optional number
        m2 = re.search(second_pattern, g)
        if m2 is not None:
          inner_bag_rule = m2.group('inner_bag_rule')
          #print(" -- Inner Bag Rule: {}".format(inner_bag_rule))
          
          # If found, further parse for the rule's bag count and color
          m3 = re.search(third_pattern, inner_bag_rule)
          if m3 is not None:
            # If pattern successful, assume bag count and color available
            inner_bag_color = m3.group('inner_bag_color')
            bag_color_rules_dict[outer_bag_color].append({
              'bag_count': int(m3.group('bag_count')),
              'bag_color': m3.group('inner_bag_color'),
            })
            if inner_bag_color not in inner_to_outer_dict:
              inner_to_outer_dict[inner_bag_color] = list()
            inner_to_outer_dict[inner_bag_color].append(outer_bag_color)
          elif inner_bag_rule == 'no other':
            # Also, handled the "no other" rule
            bag_color_rules_dict[outer_bag_color].append({
              'bag_count': 0,
              'bag_color': "",
            })
            if "" not in inner_to_outer_dict:
              inner_to_outer_dict[""] = outer_bag_color
          else:
            # Handle rules not caught by third pattern
            print("****Pattern 3 not matched: {}".format(inner_bag_rule), file=sys.stderr)
        else:
          # Handle rules not caught by second pattern
          print("****Pattern 2 not matched: {}".format(g), file=sys.stderr)
    else:
      # Handle rules not caught by first pattern
      if len(r) > 0:
        # Only if not empty
        print("****Pattern 1 not matched: {}".format(r), file=sys.stderr)
      
  return bag_color_rules_dict, inner_to_outer_dict


def print_bag_color_rules(bag_color_rules_dict):
  for outer_bag_color, inner_rules in bag_color_rules_dict.items():
    print("Outer Bag Color: {}".format(outer_bag_color))
    for rule in inner_rules:
      print(" - Inner Bag Count: {:2}\tInner Bag Color: {}".format(rule['bag_count'], rule['bag_color']))


def count_available_outer_bag_colors(inner_to_outer_dict, my_bag_color):

  outer_bag_color_count = 0
  visited_set = set()
  discover_set = set()
  discover_set.add(my_bag_color)
  while len(discover_set) > 0:
    search_color = discover_set.pop()
    visited_set.add(search_color)
    if search_color in inner_to_outer_dict:
      for c in inner_to_outer_dict[search_color]:
        discover_set.add(c)
        print("Color {} to color {}".format(search_color, c))
        
  return len(visited_set) - 1
        
  


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  parser.add_argument("bag_color", type=str)
  args = parser.parse_args()

  assert(os.path.exists(args.input_filename))

  data = None
  with open(args.input_filename, 'r') as ifile:
    data = ifile.read().split('\n')

  bag_color_rules_dict, inner_to_outer_dict = extract_color_rules(data)
  print_bag_color_rules(bag_color_rules_dict)
  print(inner_to_outer_dict)
  
  outer_bag_color_count = count_available_outer_bag_colors(inner_to_outer_dict, args.bag_color)
  print("Available outer bag colors: {}".format(outer_bag_color_count))


if __name__ == '__main__':
  main()
