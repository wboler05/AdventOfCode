#!/usr/bin/env python3

import argparse, os, sys
import re

import numpy as np
import tqdm

def load_data(input_filename):
    # Get Raw data text
    data = None
    with open(input_filename, 'r') as ifile:
        data = ifile.read().split('\n\n')
        data = [d for d in data if len(d) > 0]

    # Extract ticket rules
    rules = {}
    rules_pattern = r"^(?P<rule_name>[\w\s]+):\s(?P<min_1>[\d]+)-(?P<max_1>[\d]+) or (?P<min_2>[\d]+)-(?P<max_2>[\d]+)$"
    for d in data[0].split('\n'):
        m = re.search(rules_pattern, d)
        if m is not None:
            rule_name = m.group('rule_name')
            min_1 = int(m.group('min_1'))
            max_1 = int(m.group('max_1'))
            min_2 = int(m.group('min_2'))
            max_2 = int(m.group('max_2'))
            rules[rule_name] = [
                (min_1, max_1),
                (min_2, max_2),
            ]

    # Extract your ticket
    your_ticket = np.array(
        [int(d) for d in data[1].split('\n')[1].split(',') if len(d) > 0]
    )

    # Extract nearby ticket matrix
    nearby_tickets = []
    for row in data[2].split('\n')[1:]:
        nearby_ticket = np.array(
            [ int(r) for r in row.split(',') if len(r) > 0]
        )
        if len(nearby_ticket) > 0:
            nearby_tickets.append(nearby_ticket)
    nearby_tickets = np.array(nearby_tickets)

    # Return dictionary on items
    return {
        'rules': rules,
        'your_ticket': your_ticket,
        'nearby_tickets': nearby_tickets,
    }

def validate_tickets(data):
    rules = data['rules']
    nearby_tickets = data['nearby_tickets']

    column_counts_set = set()
    for ticket in nearby_tickets:
        column_counts_set.add(len(ticket))
    column_count = max(column_counts_set)

    valid_tickets = list()
    error_rate = 0
    for ticket in tqdm.tqdm(nearby_tickets):
        valid_ticket_flag = True
        for column in ticket:
            valid_column_flag = False
            for rule_name, rule_parts in rules.items():
                for r in rule_parts:
                    valid_column_flag |= column >= r[0] and column <= r[1]
            if not valid_column_flag:
                print("Invalid Column: {}".format(column))
                valid_ticket_flag = False
                error_rate += column
        if valid_ticket_flag:
            valid_tickets.append(ticket)
    return np.array(valid_tickets), error_rate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    data = load_data(args.input_filename)
    valid_tickets, error_rate = validate_tickets(data)
    print("Error Rate: {}".format(error_rate))

if __name__ == '__main__':
    main()