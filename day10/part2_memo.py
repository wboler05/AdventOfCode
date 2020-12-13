#!/usr/bin/env python

# I found a solution online that uses memoization, so wanted to explore how it works

import argparse, os, sys
from part2 import load_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    data = load_data(args.input_filename)[1:]

    memo = {0: 1}
    for d in data:
        memo[d] = memo.get(d-1, 0) + memo.get(d-2, 0) + memo.get(d-3, 0)
    
    print("Total: {}".format(memo[data[-1]]))