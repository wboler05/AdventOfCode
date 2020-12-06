#!/usr/bin/env python3

import argparse, os, sys

def intersection(set_list):
  r = set()
  if len(set_list) > 0:
    r = set_list[0]
  for s in set_list:
    r &= s
  return r
  

def count_answers(group_answers):
  answers_counts = list()
  total_answers = 0
  for g in group_answers:
    answers = [set(a) for a in g if len(set(a)) > 0]
    answers_set = intersection(answers)
    group_count = len(answers_set)
    print("*******************")
    print("Answers: {}".format(answers))
    print("Answers Set: {}".format(answers_set))
    print("Group Count: {}".format(group_count))
    answers_counts.append({
      'answers': answers,
      'answers_set': answers_set,
      'group_count': group_count
    })
  return {
    'answers_counts': answers_counts,
    'total_answers': sum([a['group_count'] for a in answers_counts]),
  }
      

def main():
  
  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  args = parser.parse_args()
  
  assert(os.path.exists(args.input_filename))
  
  data = None
  with open(args.input_filename, 'r') as ifile:
    data = ifile.read().split('\n\n')
  
  group_answers = list()
  for d in data:
    if len(d) == 0:
      continue
    answers = d.split('\n')
    group_answers.append(answers)
    
  answer_counts_dict = count_answers(group_answers)
  print("Total Answers Yes: {}".format(answer_counts_dict['total_answers']))
  

if __name__ == '__main__':
  main()
