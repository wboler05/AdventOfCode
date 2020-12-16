#!/usr/bin/env python3

import argparse, os, sys
import re

class Passport(object):
  expected_params = expected_params = set([
      'byr', 'iyr', 'eyr', 'hgt',
      'hcl', 'ecl', 'pid', 'cid'
    ])

  def __init__(self, msg_str="", verbose=False):
    self.param_dict = dict()
    self.found_params = dict()
    self.valid_ = False
    self.parse_msg(msg_str, verbose)

  def parse_msg(self, msg_str, verbose=False):
    self.param_dict = dict()
    # Split string on white space
    self.found_params = dict()
    for p in self.expected_params:
      self.found_params[p] = False

    # Airport hack!!
    self.found_params['cid'] = True

    params = msg_str.split()
    for p in params:
      param_key, value = p.split(':')
      if param_key in self.expected_params:
        self.param_dict[param_key] = value
        self.found_params[param_key] = True
    self.validate(verbose)


  def validate(self, verbose=False):
    self.valid_ = all(self.found_params.values())
    if not self.valid_:
      if verbose:
        print("Invalid: Not all params present")
      return

    # More advanced fun stuff

    # byr
    try:
      byr = int(self.param_dict['byr'])
      if byr < 1920 or byr > 2002:
        if verbose:
          print("Invalid: byr: {}".format(byr))
        self.valid_ = False
        #return
    except ValueError:
      if verbose:
        print("Invalid: byr Value Error: {}".format(self.param_dict['byr']))
      self.valid_ = False
      #return
    except Exception:
      raise

    # iyr
    try:
      iyr = int(self.param_dict['iyr'])
      if iyr < 2010 or iyr > 2020:
        if verbose:
          print("Invalid: iyr: {}".format(iyr))
        self.valid_ = False
        #return
    except ValueError:
      if verbose:
        print("Invalid: iyr Value Error: {}".format(self.param_dict['iyr']))
      self.valid_ = False
      #return
    except Exception:
      raise

    #eyr
    try:
      eyr = int(self.param_dict['eyr'])
      if eyr < 2020 or eyr > 2030:
        if verbose:
          print("Invalid: eyr: {}".format(eyr))
        self.valid_ = False
        #return
    except ValueError:
      if verbose:
        print("Invalid: eyr Value Error: {}".format(self.param_dict['eyr']))
      self.valid_ = False
      #return
    except Exception:
      raise
    
    
    #hgt
    hgt_pattern = "^([\d]+)([\w]+)$"
    hgt = self.param_dict['hgt']
    hgt_m = re.search(hgt_pattern, hgt)
    if hgt_m is None:
      if verbose:
        print("Invalid: hgt does not match pattern: {}".format(hgt))
      self.valid_ = False
    else:
      height, scale = hgt_m.groups()
      try:
        height = int(height)
      except ValueError:
        if verbose:
          print("Invalid: hgt height is not integer: {}".format(hgt))
        self.valid_ = False
      except Exception:
        raise

      if scale not in set(['cm', 'in']):
        if verbose:
          print("Invalid: hgt invalid scale: {}, scale({})".format(hgt, scale))
        self.valid_ = False
      else:
        if scale == 'cm':
          if height < 150 or height > 193:
            if verbose:
              print("Invalid: hgt height is off scale: {}".format(hgt))
            self.valid_ = False
        elif scale == 'in':
          if height < 59 or height > 76:
            if verbose:
              print("Invalid: hgt height is off scale: {}".format(hgt))
            self.valid_ = False
          
    #hcl
    hcl_pattern = "^(?:\#)([a-fA-F0-9]+)$"
    hcl_m = re.search(hcl_pattern, self.param_dict['hcl'])
    if hcl_m is None:
      if verbose:
        print("Invalid: hcl does not match pattern: {}".format(self.param_dict['hcl']))
      self.valid_ = False
    else:
      hcl = hcl_m.groups()[0]
      if len(hcl) != 6:
        print("Invalid: hcl has invalid length: {}".format(hcl))

    #ecl
    ecl_set = set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
    ecl = self.param_dict['ecl']
    if ecl not in ecl_set:
      if verbose:
        print("Invalid: ecl not in set: {} of {}".format(ecl, ecl_set))
      self.valid_ = False
      #return

    #pid
    if len(self.param_dict['pid']) != 9:
      if verbose:
        print("Invalid: pid length != 9: {}".format(self.param_dict['pid']))
      self.valid_ = False
      #return

    #cid
    #Ignore...


  def __str__(self):
    return "( params: {}, valid: {} )".format(self.param_dict, self.valid_)

def parse_passport_file(input_filename, verbose=False):

  assert(os.path.exists(input_filename))
  data = None
  with open(input_filename, 'r') as ifile:
    data = ifile.read().split('\n\n')

  passport_list = list()
  for d in data:
    p = Passport(d, verbose)
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
