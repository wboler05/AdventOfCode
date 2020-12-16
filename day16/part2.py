#!/usr/bin/env python3

import argparse, os, sys
from part1 import load_data, validate_tickets

import numpy as np
import tqdm
import re

def determine_column_rules(data, valid_tickets):
    rules = data['rules']
    column_count = valid_tickets.shape[1]

    column_rule_set = [ set(rules.keys()) for i in range(column_count)]

    discover_columns = set(range(column_count))
    found_columns = set()

    for ticket in valid_tickets:
        for column_idx in discover_columns:
            potential_rules = column_rule_set[column_idx]
            if len(potential_rules) == 1 or column_idx in found_columns:
                found_columns.add(column_idx)
                continue
            else:
                column = ticket[column_idx]
                bad_rules = set()
                for rule_key in potential_rules:
                    rule = rules[rule_key]
                    valid_rule = False
                    for r in rule:
                        valid_rule |= column >= r[0] and column <= r[1]
                    if not valid_rule:
                        bad_rules.add(rule_key)
                potential_rules -= bad_rules
            column_rule_set[column_idx] = potential_rules

    # Process of elimination
    found_rules = set()
    while len(found_rules) != column_count:
        found_rule_prev_len = len(found_rules)
        for rule_set in column_rule_set:
            if len(rule_set) == 1:
                found_rules.add(list(rule_set)[0])
        for i in range(len(column_rule_set)):
            if len(column_rule_set[i]) > 1:
                column_rule_set[i] -= found_rules
        if len(found_rules) == found_rule_prev_len:
            break

    for rule_set in column_rule_set:
        assert(len(rule_set) == 1)
    
    column_rules = [ list(rule_set)[0] for rule_set in column_rule_set ]
    return column_rules

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    data = load_data(args.input_filename)
    valid_tickets, _ = validate_tickets(data)
    column_rules = determine_column_rules(data, valid_tickets)
    print(column_rules)

    my_ticket = data['your_ticket']
    print("My Ticket: {}".format(my_ticket))
    value = 1
    count = 0
    for idx, rule_key in enumerate(column_rules):
        #print(idx, rule_key)
        if rule_key.startswith("departure"):
            value *= my_ticket[idx]
            count += 1
    print("Count: {}".format(count))
    print("Multiplier: {}".format(value))
        

if __name__ == '__main__':
    main()

