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
      #print("Entry: {}, Groups: {}".format(entry, m.groupdict()))
      gd = m.groupdict()

      password = gd['password']
      first = int(gd['min']) - 1
      second = int(gd['max']) - 1

      first_match = False
      if first < len(password) and first >= 0:
        first_match = password[first] == gd['letter']
      second_match = False
      if second < len(password) and second >= 0:
        second_match = password[second] == gd['letter']
      valid = ((not first_match) and (second_match)) or ((first_match) and (not second_match))
      valid_entries_truth.append(valid)
      if first_match or second_match:
        print("Entry: {}, Groups: {}".format(entry, m.groupdict()))
        print(" - Valid: {}".format(valid))
        print(" - First Valid: {}".format(first_match))
        print(" - Second Valid: {}".format(second_match))

    else:
      print("No pattern match: {}".format(entry))

  print("Valid Passwords: {}".format(sum(valid_entries_truth)))    
