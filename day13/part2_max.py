#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import time
import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", type=str)
    parser.add_argument('--reversed', '-r', action='store_true')
    args = parser.parse_args()

    time_start = time.clock()

    data = None
    with open(args.input_filename, 'r') as ifile:
        data = ifile.read().split('\n')[1].split(',')
        data = [d for d in data if len(d) > 0]
    print("Data: {}".format(data))

    numbers = [ int(d) for d in data if d != 'x']
    shifts = { int(d): i for i,d in enumerate(data) if d != 'x'}

    print("Numbers: {}\nShifts: {}".format(numbers, shifts))
    
    max_number = np.max(numbers)
    max_shift = shifts[max_number]
    print("Max Number: {},\t Shift: {}".format(max_number, max_shift))

    max_timestamp = 1
    for n in numbers:
        max_timestamp *= n
    min_timestamp = max_timestamp / np.min(numbers)

    print("Max Timestamp: {}".format(max_timestamp))

    p = tqdm.tqdm(total=max_timestamp)
    p.update(min_timestamp)

    idx = int(min_timestamp / max_number)
    if args.reversed:
        idx = int(max_timestamp / max_number)
    #idx = 0
    earliest_timestamp = None
    while idx >= 1:
        p.update(1)
        mth_time_stamp = idx * max_number
        time_stamp = mth_time_stamp - max_shift
        valid = True
        for n in numbers:
            if (time_stamp + shifts[n]) % n != 0:
                valid = False
                break
        if valid:
            earliest_timestamp = time_stamp
            break
        if args.reversed:
            idx -= 1
        else:
            idx += 1
    p.close()

    print("Earliest Timestamp: {}".format(earliest_timestamp))    

    time_end = time.clock()
    print("Elapsed Time: {} seconds".format(time_end - time_start))