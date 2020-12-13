#!/usr/bin/env python

import argparse, os, sys
import numpy as np

def calc_ratios(data):
    d = data[0]
    return np.divide(d, data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", type=str)
    args = parser.parse_args()

    data = None
    with open(args.input_filename, 'r') as ifile:
        data = ifile.read().split('\n')[1].split(',')
        data = [d for d in data if len(d) > 0]
    print(data)

    '''
    i = 0
    earliest_timestamp = None
    while earliest_timestamp is None:
        valid = True
        for j,rule in enumerate(data):
            if rule == 'x':
                continue
            elif j+i % int(rule) != 0:
                valid = False
                break
        if valid:
            earliest_timestamp = i
            break
        else:
            i += 1
    print("Earliest Timestamp: {}".format(earliest_timestamp))
    '''
    

    
    import tqdm

    bus_id_dict = {}
    for i,d in enumerate(data):
        if d != 'x':
            bus_id_dict[i] = int(d)

    print([d for d in bus_id_dict.values()])

    p = tqdm.tqdm()
    i = 1
    print("Start Multiple: {}".format(i))
    earliest_timestamp = None
    while earliest_timestamp is None:
        p.update(1)
        val = int(data[0]) * i
        valid = True
        for k,d in bus_id_dict.items():
            if (val + k) % d != 0:
                valid = False
        if not valid:
            i += 1
        else:
            earliest_timestamp = val
    p.close()
    print("Earliest Time Stamp: {}".format(earliest_timestamp))
    


    


if __name__ == '__main__':
    main()