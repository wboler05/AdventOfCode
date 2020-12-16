#!/usr/bin/env python3

import argparse, os, sys

class Passport(object):
  def __init__(self, msg_str=""):
    self.param_dict = dict()
    self.valid_ = False
    self.parse_msg(msg_str)

  def parse_msg(self, msg_str):
    self.param_dict = dict()
    # Split string on white space
    expected_params = set([
      'byr', 'iyr', 'eyr', 'hgt',
      'hcl', 'ecl', 'pid', 'cid'
    ])
    found_param = dict()
    for p in expected_params:
      found_param[p] = False

    # Airport hack!!
    found_param['cid'] = True

    params = msg_str.split()
    for p in params:
      param_key, value = p.split(':')
      if param_key in expected_params:
        self.param_dict[param_key] = value
        found_param[param_key] = True
    self.valid_ = all(found_param.values())

  def __str__(self):
    return "( params: {}, valid: {} )".format(self.param_dict, self.valid_)

def parse_passport_file(input_filename, verbose=False):

  assert(os.path.exists(input_filename))
  data = None
  with open(input_filename, 'r') as ifile:
    data = ifile.read().split('\n\n')

  passport_list = list()
  for d in data:
    p = Passport(d)
    passport_list.append(p)
    if verbose:
      print("Message: {}\nPassport: {}".format(d, p))

  return passport_list


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("input_file",type=str)
  parser.add_argument("--verbose", "-v", action='store_true')
  args = parser.parse_args()

  passport_list = parse_passport_file(args.input_file, args.verbose)
  print("Passport Count: {}".format(len(passport_list)))
  valid_passport_count = len([p for p in passport_list if p.valid_])
  print("Valid Passport Count: {}".format(valid_passport_count))

if __name__ == '__main__':
  main()
