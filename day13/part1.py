#!/usr/bin/env python

import argparse, os, sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    assert(os.path.exists(args.input_filename))

    data = None
    with open(args.input_filename, 'r') as ifile:
        data = ifile.read().split('\n')

    assert(data is not None)
    assert(len(data) >= 2)

    earliest_timestamp = int(data[0])
    bus_list = [int(b) for b in data[1].split(',') if b != 'x']

    bus_id = None
    done = False
    i = earliest_timestamp
    while bus_id is None:
        print(i)
        for b in bus_list:
            print(" - {}, {}".format(b, i % b))
            if i % b == 0:
                print(b)
                bus_id = (b, i)
                break
        if done:
            break
        i += 1
    
    print("Bus ID: {}".format(bus_id[0]))
    print("Time: {}".format(bus_id[1]))
    print("Multiple: {}".format(bus_id[0]*(bus_id[1]-earliest_timestamp)))
        
    

if __name__ == '__main__':
    main()