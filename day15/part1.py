#!/usr/bin/env python3

import argparse, os, sys
import numpy as np

def load_data(input_filename):
    assert(os.path.exists(input_filename))
    data = None
    with open(input_filename, 'r') as ifile:
        data = ifile.read().split('\n')[0].split(',')
        data = [int(d) for d in data if len(d) > 0]
    assert(len(data) > 0)
    return data


def update_memo(memo):
    for k,v in memo.items():
        memo[k] += 1
    return memo

def get_nth_number(input_vec, n):
    #print("Input Vector: {}".format(input_vec))
    memo = {}
    cur_num = None
    for i in range(n-1):
        if i < len(input_vec):            
            cur_num = input_vec[i]

        #print("Turn({}): Current Number: {}".format(i+1, cur_num))
        if cur_num not in memo:
            #print(" - Not seen")
            memo[cur_num] = 0
            cur_num = 0
            #if i < len(input_vec):
            #    print(" - Load Value")
        else:
            delta = memo[cur_num]
            #print(" - Delta: {}".format(delta))
            memo[cur_num] = 0
            cur_num = delta
        memo = update_memo(memo)
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