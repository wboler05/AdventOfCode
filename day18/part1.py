#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import re


def perform(operator, l_val, r_val):
    assert(operator is not None)
    if operator == '*':
        return l_val * r_val
    elif operator == '-':
        return l_val - r_val
    elif operator == '+':
        return l_val + r_val

def evaluate(expression):
    
    i = 0
    l_val = None
    operator = None
    while i < len(expression):
        e = list(expression)[i]
        if e == '(':
            r_val, i_extension = evaluate(expression[i+1:])
            i += i_extension
            if l_val is None:
                l_val = r_val
            else:
                assert(operator is not None)
                l_val = perform(operator, l_val, r_val)
                operator = None

        elif e == ')':
            return l_val, i+1
        elif e == ' ':
            pass
        elif e in { '*', '-', '+' }:
            operator = e
        else:
            m = re.search(r'(?P<val>[\d]+)', str(list(expression)[i:]))
            if m is not None:
                val = m.group('val')
                i += len(val) - 1
                val = int(val)
                if l_val is None:
                    l_val = val
                else:
                    l_val = perform(operator, l_val, val)
                    operator = None
        i = i + 1
    return l_val, i-1



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
        r = evaluate(expression)[0]
        s += r
        print("{} = {}".format(expression, r))
    print("Sum :: {}".format(s))

    


if __name__ == '__main__':
    main()