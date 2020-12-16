#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import tqdm

def load_data(input_filename):
    assert(os.path.exists(input_filename))
    data = None
    with open(input_filename, 'r') as ifile:
        data = ifile.read().split('\n')[0].split(',')
        data = [int(d) for d in data if len(d) > 0]
    assert(len(data) > 0)
    return data
    

def get_nth_number(input_vec, n):
    memo = {}
    cur_num = None
    for i in tqdm.tqdm(range(n-1)):
        if i < len(input_vec):            
            cur_num = input_vec[i]
        if cur_num not in memo:
            memo[cur_num] = i
            cur_num = 0
        else:
            delta = i - memo[cur_num]
            memo[cur_num] = i
            cur_num = delta
    return cur_num

def get_2020th_number(input_vec):
    return get_nth_number(input_vec, 2020)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    parser.add_argument('-n', type=int, default=2020)
    args = parser.parse_args()

    data = load_data(args.input_filename)
    print("Starting Data: {}".format(data))
    num = get_nth_number(data, args.n)
    print("{}th Number: {}".format(args.n, num))

if __name__ == '__main__':
    main()