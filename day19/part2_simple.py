#!/usr/bin/env python

import argparse, os, sys
import re
import numpy as np

import tqdm

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

rule_8 = set()
rule_11 = set()

def build_rule_8(rules, max_size):
    global rule_8

    print("Max Size: {}".format(max_size))

    rule = rules['8']
    rule_42 = expand_rules(rules, 42, max_size)
    rule_set = rule_42.copy()
    max_len = 0
    discover = rule_set.copy()
    while True:
        break_flag = False
        for r in rule_set:
            discover.add(r)
            if len(r) >= max_size:
                break_flag = True
                break
        if break_flag:
            break
        growth_set = set()
        print("Len: {}".format(len(rule_set)))
        for r in tqdm.tqdm(rule_set):
            if r in discover:
                discover.remove(r)
                for r2 in rule_42:
                    s = r + r2
                    discover.add(s)
                    if len(s) > max_size:
                        break
                    if len(s) > max_len:
                        max_len = len(s)
                        print("Max Change: {}".format(max_len))
                    growth_set.add(r + r2)
        if len(growth_set) > 0:
            rule_set |= growth_set
        else:
            break


    final_rule_set = set()
    for r in rule_set:
        final_rule_set.add(r[:max_size])
    rule_8 = final_rule_set


def build_rule_11(rules, max_size):
    global rule_11

    rule = rules['11']
    rule_42 = expand_rules(rules, 42, max_size)
    rule_31 = expand_rules(rules, 31, max_size)

    rule_set = set()
    discover = set()

    for r42 in rule_42:
        for r31 in rule_31:
            s = r42 + r31
            if len(s) <= max_size:
                rule_set.add(s)
                discover.add(s)

    while len(discover) > 0:
        
        right_set = rule_set.copy()
        for r in tqdm.tqdm(right_set):
            if r not in discover:
                continue
            for r42 in rule_42:
                for r31 in rule_31:
                    s = r42 + r + r31
                    if len(s) <= max_size:
                        if s not in rule_set:
                            rule_set.add(s)
                            discover.add(s)
                        else:
                            discover.remove(s)

        for r42 in tqdm.tqdm(rule_42):
            for r31 in rule_31:
                s = r42 + r31
                if len(s) <= max_size:
                    if s not in rule_set:
                        rule_set.add(s)
                        discover.add(s)
                    else:
                        discover.remove(s)

    rule_11 = rule_set


def expand_rules(rules, rule_idx, max_size):

    if rule_idx == 0:
        raise Exception("Error, Rule 0 is handled seperately")

    rule = rules[str(rule_idx)]
    if 'letter' in rule:
        return rule['letter']
    else:
        rule_set = set()
        for rule_list in rule['rule_list']:
            sub_rule_set = ['']
            for component in rule_list:
                r_val = None
                if component == '8':
                    #r_val = rule_8
                    #r_val = set(["{rule_8}"])
                    raise Exception("Rule 8 found")
                elif component == '11':
                    #r_val = rule_11
                    #r_val = set(["{rule_11}"])
                    raise Exception("Rule 11 found")
                else:
                    r_val = expand_rules(rules, component, max_size)
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
        return rule_set

def handle_rule_0(rules, msg_data):

    # 0: 8 11

    max_size = max([len(d) for d in msg_data])

    rule_42_set = expand_rules(rules, 42, max_size)
    rule_31_set = expand_rules(rules, 31, max_size)

    discover_8 = rule_42_set.copy()
    discover_11 = rule_42_set.copy()
    rule_set = set()
    
    valid_8 = set()
    valid_11 = set()

    msg_42_set = set(msg_data)
    cache = set()
    while len(msg_42_set) > 0:
        m = msg_42_set.pop()
        for r42 in rule_42_set:
            if m.startswith(r42):
                cache.add(m)
    msg_42_set = cache.copy()
    print(len(msg_42_set), len(msg_data))

    # Find all Rule 8 matches
    while len(discover_8):
        # Match rule 8
        # 8: 42 | 42 8
        found_8 = set()
        cache = set()
        for m in tqdm.tqdm(msg_42_set):
            msg_found = False
            for search in discover_8:
                if m.startswith(search):
                    found_8.add(search)
                    valid_8.add(search)
                    msg_found = True
                    #print(search, m)
            if msg_found:
                cache.add(m)
        msg_42_set = cache.copy()
        print("MSG 42 Len: {}".format(len(msg_42_set)))
            
        discover_8 = set()
        for r42 in rule_42_set:
            for f in found_8:
                s = r42 + f
                if len(s) <= max_size:
                    discover_8.add(s)
        print(" - Found 8: {}".format(len(found_8)))
        print(" - Discover 8 length: {}".format(len(discover_8)))

    print("Valid 8: {}".format(len(valid_8)))

    discover_11_42 = set()
    valid_msg_set = set()
    msg_42_set = set()
    for m in tqdm.tqdm(msg_data):
        for v8 in valid_8:
            for r42 in rule_42_set:
                s = v8 + r42
                if len(s) <= max_size:
                    if m.startswith(s):
                        msg_42_set.add(m)
                        discover_11_42.add(s)
    cache = set()
    for m in msg_42_set:
        for r31 in rule_31_set:
            if m.endswith(r31):
                cache.add(m)
    msg_42_set = cache.copy()
    print("Msg 42 to 11 Start Set: {}".format(len(msg_42_set)))
    print("Discover 11 - 42 Set: {}".format(len(discover_11_42)))

    # 0: 8 11
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    valid_msg_set =set()
    for m in msg_42_set:
        v = m
        match_31 = True
        r31_count = 0
        while match_31:
            match_31 = False
            for r31 in rule_31_set:
                if v.endswith(r31):
                    v = v[:-len(r31)]
                    match_31 = True
                    r31_count += 1
                    break
        r42_count = 0
        while len(v) > 0:
            found_42 = False
            for r42 in rule_42_set:
                if v.endswith(r42):
                    v = v[:-len(r42)]
                    found_42 = True
                    r42_count += 1
                    break
            if not found_42:
                break

        print("R31({}), R42({}): {}".format(r31_count, r42_count, m))
        if len(v) == 0 and r42_count >= 2 and (r42_count - r31_count) >= 1:
            valid_msg_set.add(m)

    print("Total Valid Messages: {}".format(len(valid_msg_set)))

    '''
    found = set()
    while len(discover_11_42) > 0:
        # Match rule 11
        # 11: 42 31 | 42 11 31
        found_11 = set()
        for search in tqdm.tqdm(discover_11_42):
            for r31 in rule_31_set:
                r11 = search + r31
                if s not in found:
                    found.add(r11)
                    if len(r11) <= max_size:
                        if r11 in msg_42_set:
                            valid_msg_set.add(r11)
                            msg_42_set.remove(r11)
                        found_11.add(r11)
                        for r42 in rule_42_set:
                            new_r11 = r42 + r11
                            if new_r11 not in found:
                                found.add(new_r11)
                                if len(new_r11) <= max_size:
                                    if new_r11 in msg_42_set:
                                        valid_msg_set.add(new_r11)
                                        msg_42_set.remove(new_r11)
                                    for m in msg_42_set:
                                        if m.startswith(r42 + search):
                                            found_11.add(new_r11)
                                            
        discover_11_42 = found_11.copy()
        print("Len Discover 11-42: {}".format(len(discover_11_42)))
        print(" - Msg Set Length: {}".format(len(msg_42_set)))
        print(" - Valid Msgs: {}".format(len(valid_msg_set)))
    '''

    valid_msg_indexes = list()
    for i,m in enumerate(msg_data):
        if m in valid_msg_set:
            valid_msg_indexes.append(i)
    return valid_msg_indexes



def process_rules(rules, msg_data, rule_numbers = [ 0 ]):
    valid_messages = set(range(len(msg_data)))

    max_msg_size = max([len(d) for d in msg_data])

    for rule_idx in rule_numbers:
        #build_rule_8(rules, max_msg_size)
        #build_rule_11(rules, max_msg_size)
        if rule_idx == 0:
            return handle_rule_0(rules, msg_data)
        else:
            valid_message_set = expand_rules(rules, rule_idx, max_msg_size)
            print("Valid Messages: {}".format(valid_message_set))
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

    rules = extract_rules(rule_data)

    valid_msgs = process_rules(rules, msg_data)
    print("Valid Messages: ")
    for v in valid_msgs:
        print(" - ({}): {}".format(v, msg_data[v]))
    print("Valid Message Count: {}".format(len(valid_msgs)))
                    


    

if __name__ == '__main__':
    main()
    