#!/usr/bin/env python3

import argparse, os, sys

def count_answers(group_answers):
  answer_counts = list()
  total_answers = 0
  for g in group_answers:
    group_answer_dict = {
      'answers': list(),
      'answer_set': set(),
      'group_count': 0
    }
    for response in g:
      answer_set = set(response)
      answer_count = len(answer_set)
      group_answer_dict['answers'].append(response)
      group_answer_dict['answer_set'] |= answer_set
    group_answer_dict['group_count'] = len(group_answer_dict['answer_set'])
    total_answers += group_answer_dict['group_count']
    answer_counts.append(group_answer_dict)
  return {
    'answer_counts': answer_counts,
    'total_answers': total_answers,
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
