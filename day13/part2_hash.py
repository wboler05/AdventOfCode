#!/usr/bin/env python

import argparse, os, sys
import numpy as np
import tqdm

def calc_ratios(data):
    d = data[0]
    return np.divide(d, data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", type=str)
    parser.add_argument("--chunk-size", "-n", type=int, default=50000)
    args = parser.parse_args()

    data = None
    with open(args.input_filename, 'r') as ifile:
        data = ifile.read().split('\n')[1].split(',')
        data = [d for d in data if len(d) > 0]
    print(data)

    chunks_n = args.chunk_size

    numbers = [int(d) for d in data if d != 'x']
    shifts = { int(d): i for i,d in enumerate(data) if d != 'x'}
    ratios = { n : float(n) / float(numbers[0]) for n in numbers }
    counts = { n : np.ceil(float(ratios[n])*float(chunks_n)).astype(int) for n in numbers }
    offset = { n : 1 for n in numbers}

    p = tqdm.tqdm()
    while True:
        p.update(counts[numbers[0]])
        arrs = { n : np.arange(offset[n], c+offset[n])*n-shifts[n] for n,c in counts.items()}
        unique, freqs = np.unique(np.hstack(list(arrs.values())), return_counts=True)
        max_freq = np.max(freqs)
        offset = { n : offset[n] + counts[n] for n in numbers}
        if max_freq == len(numbers):
            idx = np.argwhere(freqs == max_freq)[0][0]
            print("Earliest Timestamp: {}".format(unique[idx]))
            break
    p.close()


    #print('shifts: {}'.format(shifts))
    #print('ratios: {}'.format(ratios))
    #print('counts: {}'.format(counts))
    #print("arrs: {}".format(arrs))


    #print("Earliest Time Stamp: {}".format(earliest_timestamp))
    


    


if __name__ == '__main__':
    main()