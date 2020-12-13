#!/usr/bin/env python3

'''
My colleague said to use graph theory...
'''

import argparse, os, sys
import numpy as np
from part2 import load_data
import tqdm
import time

def count_all_paths(edges, start_node, end_node):
    path_count = 0

    if start_node == end_node:
        #print("\n", end="")
        return 1
    #print("{}->".format(start_node), end="")

    if start_node not in edges:
        return 0
    else:
        nodes = [n[0] for n in edges[start_node]]
        for node in nodes:
            path_count += count_all_paths(edges, node, end_node)
    return path_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename')
    parser.add_argument('-n', type=int, default=None)
    args = parser.parse_args()

    data = load_data(args.input_filename)
    assert(data is not None)
    print("Data: {}".format(len(data)))

    if args.n is not None:
        n = min(len(data), max(args.n, 0))
        data = data[:n]

    nodes = set(list(data))
    start_node = np.min(data)
    end_node = np.max(data)

    start_time = time.clock()

    # build edge_list
    edges = dict()
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            left = data[i]
            right = data[j]
            diff = right-left
            if diff <= 3 and diff > 0:
                if left not in edges:
                    edges[left] = list()
                edges[left].append((right, diff))

    #for left,v in edges.items():
    #    for (right, diff) in v:
    #        print("Left({}) -> Right({}): {}".format(left, right, diff))

    # Find all paths from min to max
    path_count = count_all_paths(edges, start_node, end_node)

    end_time = time.clock()
    print("Time: {} seconds".format(end_time - start_time))

    print("Path Count: {}".format(path_count))

        