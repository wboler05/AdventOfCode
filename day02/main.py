#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import re

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument('input_filename', type=str, help="Input file of passwords (.txt)")

  args = parser.parse_args()

  assert(os.path.exists(args.input_filename))

  data = None
  with open(args.input_filename, 'r') as ifile:
    data = np.array(ifile.read().split('\n'))[:-1]

  print('Password count: {}'.format(len(data)))

  pattern = '^(?P<min>[\d]+)(?:-)(?P<max>[\d]+)(?:\s)(?P<letter>[\w]+):(?:\s)(?P<password>[\S]+)$'

  valid_entries_truth = list()
  for entry in data:
    
    m = re.match(pattern, entry)
    if m is not None:
      print("Entry: {}, Groups: {}".format(entry, m.groupdict()))
      gd = m.groupdict()
      pass_set = set(gd['password'])
      counts = dict()
      print(" - Password Set: {}".format(pass_set))
      for p in pass_set:
        counts[p] = gd['password'].count(p)
      print(counts)
      is_valid = True
      for c in gd['letter']:
        if gd['letter'] not in pass_set:
          is_valid = False
          break
        if counts[gd['letter']] < int(gd['min']):
          is_valid = False
          break
        if counts[gd['letter']] > int(gd['max']):
          is_valid = False
          break
        valid_entries_truth.append(is_valid)
    else:
      print("No pattern match: {}".format(entry))

  print("Valid Passwords: {}".format(sum(valid_entries_truth)))    
