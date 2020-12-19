#!/usr/bin/env python

import argparse, os, sys
import re

def load_data(input_filename):
    data = None
    assert(os.path.exists(input_filename))
    with open(input_filename, 'r') as ifile:
        data = [d for d in ifile.read().split('\n\n') if len(d) > 0]
        print(len(data))

    rule_data = [ d for d in data[0].split('\n') if len(d) > 0 ]
    msg_data = [ d for d in data[1].split('\n') if len(d) > 0 ]

    return {
        "rule_data": rule_data,
        "msg_data": msg_data,
    }

def extract_rules(rule_data):
    master_rule_pattern = r"^(?P<rule_number>[\d]+): (?P<rule_text>[\w\s\d|\"]+)$"
    inner_rule_letter_pattern = r"^(?:\")(?P<rule_letter>[\w])(?:\")$"

    rules = dict()
    for row in rule_data:
        m = re.search(master_rule_pattern, row)
        if m is not None:
            rule_number = m.group("rule_number")
            rule_text = m.group("rule_text")
            letter_m = re.search(inner_rule_letter_pattern, rule_text)
            if letter_m is not None:
                letter = letter_m.group("rule_letter")
                rules[rule_number] = {
                    'letter': letter
                }
            else:
                optional_rules = rule_text.split('|')
                rule_list = list()
                for r in optional_rules:
                    sub_rule_list = r.split(' ')
                    sub_rule_list = [ s for s in sub_rule_list if len(s) > 0 ]
                    rule_list.append(sub_rule_list)
                rules[rule_number] = {
                    'rule_list': rule_list
                }

    return rules


def expand_rules(rules, rule_idx, max_message_size):
    rule = rules[str(rule_idx)]
    if 'letter' in rule:
        return rule['letter']
    else:
        rule_set = set()
        for rule_list in rule['rule_list']:

            for r in rule_set:
                if len(r) > max_message_size:
                    break

            sub_rule_set = ['']
            for component in rule_list:
                r_val = expand_rules(rules, component, max_message_size)
                if isinstance(r_val, str):
                    for i, r in enumerate(sub_rule_set):
                        sub_rule_set[i] += r_val
                elif isinstance(r_val, set):
                    blind = sub_rule_set
                    sub_rule_set = list()
                    for i, b in enumerate(blind):
                        for s in r_val:
                            sub_rule_set.append(b + s)

            rule_set |= set(sub_rule_set)
        new_rule_set = set()
        for r in rule_set:
            new_rule_set.add(r[:max_message_size])
        return new_rule_set


def process_rules(rules, msg_data, max_message_size, rule_numbers = [ 0 ]):
    valid_messages = set(range(len(msg_data)))

    for rule_idx in rule_numbers:
        valid_message_set = expand_rules(rules, rule_idx, max_message_size)
        for i,msg in enumerate(msg_data):
            if msg not in valid_message_set:
                valid_messages.remove(i)
    
    return valid_messages



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    parser.add_argument('--rule-number', '-r', nargs="+", type=int, default=[0])
    args = parser.parse_args()

    data = load_data(args.input_filename)

    rule_data = data['rule_data']
    msg_data = data['msg_data']

    max_msg_size = max([len(d) for d in msg_data])

    rules = extract_rules(rule_data)

    valid_msgs = process_rules(rules, msg_data, max_msg_size, args.rule_number)
    print("Valid Messages: ")
    for v in valid_msgs:
        print(" - ({}): {}".format(v, msg_data[v]))
    print("Valid Message Count: {}".format(len(valid_msgs)))
                    


    

if __name__ == '__main__':
    main()
    