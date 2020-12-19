#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import re

from part1 import evaluate

def change_order_operations(expression):
    e_cache = expression
    i = 0
    num_pos = None
    operator_found = False
    while (i < len(e_cache)):
        e = e_cache[i]
        if e == '(':
            new_expression, new_i = change_order_operations(e_cache[i+1:])
            e_cache = e_cache[:i+1] + new_expression
            if not operator_found and num_pos is None:
                num_pos = i+1
            i += new_i
        elif e == ')':
            if operator_found and num_pos is None:
                e_cache = e_cache[:i] + ')' + e_cache[i:]
                i += 1
            return e_cache, i+1
        elif e == ' ':
            pass
        elif e == '+':
            if operator_found:
                pass
            else:
                operator_found = True
                if num_pos is not None:
                    e_cache = e_cache[:num_pos] + '(' + e_cache[num_pos:]
                    num_pos = None
                    i += 1
                else:
                    pass
        elif e == '*':
            if operator_found:
                e_cache = e_cache[:i-1] + ')' + e_cache[i-1:]
                operator_found = False
                i += 1
            else:
                num_pos = None
        else:
            if not operator_found:
                m = re.search(r'(?P<val>[\d]+)', e_cache[i:])
                if m is not None:
                    num_pos = i
                    i += len(m.group('val')) - 1
        i += 1
    if operator_found:
        e_cache += ')'
    return e_cache, i
            



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", type=str)
    args = parser.parse_args()

    data = None
    with open(args.input_filename, 'r') as ifile:
        data = ifile.read().split('\n')
        data = [d for d in data if len(d) > 0]

    s = 0
    for expression in data:
        new_expression = change_order_operations(expression)[0]
        r = evaluate(new_expression)[0]
        s += r
        print("{} = {}".format(expression, r))
    print("Sum :: {}".format(s))

    


if __name__ == '__main__':
    main()