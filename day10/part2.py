#!/usr/bin/env python3

'''
There's got to be something smarter than a bruteforce search.
'''

import argparse, os, sys
import numpy as np

class HashSet(object):
    def __init__(self):
      self.hash = dict()
      
    def __iter__(self):
      for k,v in self.hash.items():
        for a in v:
          if len(a) > 0:
            yield a
      
    def key(self, obj):
      return hash(np.array(obj).tobytes())

    def add(self, obj):
      key = self.key(obj)
      if key not in self.hash:
        self.hash[key] = list()
      for item in self.hash[key]:
        if np.all(item == obj):
          return
      self.hash[key].append(obj)

    def __contains__(self, obj):
      key = self.key(obj)
      if key not in self.hash:
        return False
      for item in self.hash[key]:
        if np.all(obj == item):
          return True
      return False
      
    def __len__(self):
      d = 0
      for k,v in self.hash.items():
        d += len(v)
      return d

    def pop(self):
      if len(self.hash) == 0:
        return None
      for k,v in self.hash.items():
        if len(v) == 0:
          self.hash[k] = None
          continue
        r_val = self.hash[k].pop()
        if len(self.hash[k]) == 0:
          self.hash.pop(k, None)
        return r_val

    def empty(self):
      if len(self.hash) == 0:
        return True
      for v in self.hash.values():
        if len(v) > 0:
          return False
      return True
    
      
    def depth(self):
      depth = 0
      for v in self.hash.values():
        depth = np.max([len(a) for a in v], depth)
      return depth
      
    def delete_taller_than(self, height):
      for k,v in self.hash.items():
        del_list = list()
        for i,a in enumerate(v):
          if len(a) > height:
            del_list.append(i)
        del_list = sorted(del_list, reversed=True)
        while len(del_list) > 0:
          idx = del_list.pop()
          del self.hash[k][idx]


def validate(data, left_val=None, right_val=None):
  if len(data) == 0:
    return False
  potential = data[0]
  if left_val is not None:
    potential = left_val
  cache = data
  if right_val is not None:
    cache = np.array(list(cache) + [right_val])
  for i in range(1,len(cache)):
    d = cache[i]
    diff = d - potential
    if diff > 3 or diff <= 0:
      return False
    potential = d
  return True
            

def load_data(input_filename):
  assert(os.path.exists(input_filename))
  data = None
  with open(input_filename, 'r') as ifile:
    data = sorted(
      np.array(
        [ d for d in ifile.read().split('\n') if len(d) > 0]
      ).astype(int)
    )
  return np.array([0] + list(data) + [np.max(data)+3])

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  args = parser.parse_args()

  data = load_data(args.input_filename)

  search_set, found_set = HashSet(), HashSet()
  search_set.add(data)
  valid_count = 0
  while not search_set.empty():
    #print("Search Length: {}".format(len(search_set)))
    #print("Found Length: {}".format(len(found_set)))
  
    search_list = search_set.pop()
    if search_list in found_set:
      continue
    else:
      found_set.add(search_list)
    if not validate(search_list):
      continue
    else:
      print("Valid: {}".format(search_list))
      valid_count += 1
      for i in range(0, len(search_list)-1):
        check_list = np.delete(search_list,i)
        if check_list not in found_set:
          if validate(check_list):
            search_set.add(check_list)
  print("Valid sets: {}".format(valid_count))
          
    
  validate(data)

if __name__ == '__main__':
  main()
