#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import tqdm

ACTIVE_STATE = '#'
INACTIVE_STATE = '.'

def load_data(input_filename):
    data = None
    with open(input_filename, 'r') as ifile:
        data = ifile.read().split('\n')
        data = [d for d in data if len(d) > 0]
        data = np.array([np.array([np.array(list(d)) for d in data])])
    return np.array([data])


def check_edge_activity(data):
    return  \
        np.all(data[0,:,:,:] == INACTIVE_STATE) and np.all(data[-1,:,:,:] == INACTIVE_STATE) and \
        np.all(data[:,0,:,:] == INACTIVE_STATE) and np.all(data[:,-1,:,:] == INACTIVE_STATE) and \
        np.all(data[:,:,0,:] == INACTIVE_STATE) and np.all(data[:,:,-1,:] == INACTIVE_STATE) and \
        np.all(data[:,:,:,0] == INACTIVE_STATE) and np.all(data[:,:,:,-1] == INACTIVE_STATE)


def add_inactive_neighbors(data):
    new_data = np.full(np.array(data.shape)+2, '.')
    new_data[1:-1, 1:-1, 1:-1, 1:-1] = data
    return new_data


def trim_fat(data):
    new_data = data.copy()

    if np.all(data[0,:,:,:] == INACTIVE_STATE):
        if new_data.shape[0] > 1:
            new_data = new_data[1:,:,:,:]

    if np.all(data[:,0,:,:] == INACTIVE_STATE):
        if new_data.shape[1] > 1:
            new_data = new_data[:,1:,:,:]

    if np.all(data[:,:,0,:] == INACTIVE_STATE):
        if new_data.shape[2] > 1:
            new_data = new_data[:,:,1:,:]

    if np.all(data[:,:,:,0] == INACTIVE_STATE):
        if new_data.shape[3] > 1:
            new_data = new_data[:,:,:,1:]


    if np.all(data[-1,:,:,:] == INACTIVE_STATE):
        if new_data.shape[0] > 1:
            new_data = new_data[:-1,:,:,:]

    if np.all(data[:,-1,:,:] == INACTIVE_STATE):
        if new_data.shape[1] > 1:
            new_data = new_data[:,:-1,:,:]

    if np.all(data[:,:,-1,:] == INACTIVE_STATE):
        if new_data.shape[2] > 1:
            new_data = new_data[:,:,:-1,:]

    if np.all(data[:,:,:,-1] == INACTIVE_STATE):
        if new_data.shape[3] > 1:
            new_data = new_data[:,:,:,:-1]

    return new_data


def activation_step(data):

    active_count  = 0
    c_data = None
    if not check_edge_activity(data):
        c_data = add_inactive_neighbors(data)
    else:
        c_data = data.copy()
    
    new_data = c_data.copy()

    for i in range(c_data.shape[0]):
        for j in range(c_data.shape[1]):
            for k in range(c_data.shape[2]):
                for w in range(c_data.shape[3]):
                    neighbor_active_count = 0
                    visits = 0
                    for m in range(max(i-1, 0), min(i+2, c_data.shape[0])):
                        for n in range(max(j-1, 0), min(j+2, c_data.shape[1])):
                            for p in range(max(k-1, 0), min(k+2, c_data.shape[2])):
                                for q in range(max(w-1, 0), min(w+2, c_data.shape[3])):
                                    visits += 1
                                    if (m == i) and (n == j) and (p == k) and (w == q):
                                        continue
                                    if c_data[m,n,p,q] == ACTIVE_STATE:
                                        neighbor_active_count += 1
                    #print("i={}, j={}, k={}, visits={}, neighbor_active_count={}, Active: {}".format(i, j, k, visits, neighbor_active_count, c_data[i, j, k]))
                    if c_data[i, j, k, w] == ACTIVE_STATE:
                        if neighbor_active_count >= 2 and neighbor_active_count <= 3:
                            #print(" - {}".format(ACTIVE_STATE))
                            new_data[i, j, k, w] = ACTIVE_STATE
                        else:
                            #print(" - {}".format(INACTIVE_STATE))
                            new_data[i, j, k, w] = INACTIVE_STATE
                    else:
                        if neighbor_active_count == 3:
                            #print(" - {}".format(ACTIVE_STATE))
                            new_data[i, j, k, w] = ACTIVE_STATE
                        else:
                            #print(" - {}".format(INACTIVE_STATE))
                            new_data[i, j, k, w] = INACTIVE_STATE
    
    new_data = trim_fat(new_data)
    return new_data


        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    parser.add_argument('-n', type=int, default=1)
    args = parser.parse_args()

    data = load_data(args.input_filename)

    for i in range(args.n):
        #print("Start Active: {}".format(np.sum(data == ACTIVE_STATE)))
        #print("{}\n\n".format(data))
        data = activation_step(data)

    print("Final Sum: {}".format(np.sum(data == ACTIVE_STATE)))
        


if __name__ == '__main__':
    main()