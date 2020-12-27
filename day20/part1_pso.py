#!/usr/bin/env python3

import argparse, os, sys
import tqdm
import numpy as np
import re
from collections import Counter, deque

from multiprocessing import Pool
from itertools import repeat

def load_data(input_filename):
    assert(os.path.exists(input_filename))
    data = None
    with open(input_filename, 'r') as ifile:
        data = [d for d in ifile.read().split('\n\n') if len(d) > 0]
    tiles = dict()
    pattern = r"^Tile (?P<tile_id>[\d]+)\:$"
    for d in data:
        grid = d.split('\n')
        m = re.search(pattern, grid[0])
        if m is not None:
            tile_id = int(m.group('tile_id'))
            grid = np.array([list(g) for g in grid[1:] if len(g) > 0])
            tiles[tile_id] = grid
        else:
            print("Unrecognized: {}".format(grid))
    return tiles


def get_row_column(idx, k):
    row = np.floor(idx / k).astype(int)
    col = idx % k
    return row, col

#memo = dict()

def fitness_function(tile_map, state):
    #global memo

    assignment_list = list()
    rotation_list = list()
    flip_list = list()
    for i in range(0, len(state), 3):
        assignment_list.append(np.floor((len(tile_map)-1) * state[i]).astype(int))
        rotation_state = state[i+1]
        flip_state = state[i+2]
        rotation_list.append(np.floor(4 * rotation_state))
        flip_list.append(np.floor(3 * flip_state))

    #memo_tuple = tuple(assignment_list) + tuple(rotation_list) + tuple(flip_list)
    #if memo_tuple in memo:
    #    return memo[memo_tuple]
    
    non_unique_penalty = 50000
    bad_assignment_penalty = 200

    total_needed_assignments = len(assignment_list)
    total_assignments = len(set(assignment_list))
    k = np.sqrt(total_needed_assignments).astype(int)

    score = total_assignments - (non_unique_penalty * (total_needed_assignments - total_assignments))
    if len(assignment_list) != len(set(assignment_list)):
        # Terminate since we've failed
        #memo[memo_tuple] = score
        return score

    tile_id_list = sorted(tile_map.keys())

    assignment_dict = dict()
    assignment_matrix = np.empty(shape=(k, k), dtype=int)
    for tile_id, idx, rotation, flip in zip(tile_id_list, assignment_list, rotation_list, flip_list):
        row, col = get_row_column(idx,k)
        assignment_dict[tile_id] = {
            'idx': idx,
            'row': row,
            'col': col,
            'rotation': rotation,
            'flip': flip
        }
        assignment_matrix[row,col] = tile_id


    # TODO just check adjacency for now
    invalid_count = list()
    available_assignments = 0
    for left_tile_id, left_mapping in tile_map.items():
        neighbors = left_mapping['neighbors']
        assignment = assignment_dict[left_tile_id]
        actual_neighbors = set()
        if (col - 1) >= 0:
            actual_neighbors.add(assignment_matrix[row, col -1])
            available_assignments += 1
        if (row - 1) >= 0:
            actual_neighbors.add(assignment_matrix[row - 1, col])
            available_assignments += 1
        if (col + 1) < k:
            actual_neighbors.add(assignment_matrix[row, col +1])
            available_assignments += 1
        if (row + 1) < k:
            actual_neighbors.add(assignment_matrix[row + 1, col])
            available_assignments += 1
        bad_assigments = actual_neighbors - neighbors
        invalid_count.append(len(bad_assigments))
    invalid_count = np.array(invalid_count)

    happiness = 500
    sadness = 150

    #score -= bad_assignment_penalty * (np.max(invalid_count) / available_assignments)
    score += happiness * np.sum(invalid_count == 0) - sadness * np.max(invalid_count)
    
    #memo[memo_tuple] = score
    return score

def get_fitness(tile_map, particles_dict):
    params = particles_dict['params']
    states = particles_dict['states']
    fitness = list()
    if params.get('pool') is None:
        for s in states:
            fitness.append(fitness_function(tile_map, s))
    elif params.get('pool') > 0:
        with Pool(params['pool']) as pool:
            fitness = pool.starmap(
                fitness_function, 
                zip(repeat(tile_map), states) 
            )
    particles_dict['fitness'] = np.array(fitness)
    return particles_dict

def fly(particles_dict):
    params = particles_dict['params']
    states = particles_dict['states']
    pb_state = particles_dict['pb_states']
    lb_state = particles_dict['lb_states']
    v = particles_dict['v']
    min_state = params['min_state']
    max_state = params['max_state']

    max_v = 0.5 * (max_state - min_state)
    min_v = -max_v

    I = (0.5 * np.random.random(states.shape) + 0.5) * v
    c1 = np.random.random(states.shape) * params['C1'] * (pb_state - states)
    c2 = np.random.random(states.shape) * params['C2'] * (lb_state - states)
    c3 = params['C3'] * (max_v - min_v) * np.random.random(states.shape)
    
    v = (I + c1 + c2 + c3) * params['dt']
    v[v > max_v] = max_v[v > max_v]
    v[v < min_v] = min_v[v < min_v]

    energy = np.sum(v**2)

    states += v

    mutation_flag = np.random.random(size=(len(states), )) < params['mutation_rate']
    states[mutation_flag] = np.random.random(states[mutation_flag].shape)

    states[states > max_state] = max_state[states > max_state]
    states[states < min_state] = min_state[states < min_state]

    particles_dict['states'] = states
    particles_dict['v'] = v
    particles_dict['energy'] = energy
    return particles_dict

def evaluate(particles_dict):
    fitness = particles_dict['fitness']
    pb_fitness = particles_dict['pb_fitness']
    lb_fitness = particles_dict['lb_fitness']
    states = particles_dict['states']
    pb_states = particles_dict['pb_states']
    lb_states = particles_dict['lb_states']

    pb_update = fitness > pb_fitness
    pb_states[pb_update] = states[pb_update]
    pb_fitness[pb_update] = fitness[pb_update]

    neighbor_size = particles_dict['params']['neighbor_size']
    half_neighbor_size = np.floor(neighbor_size / 2).astype(int)
    new_lb_fitness = lb_fitness.copy()
    for i,fit in enumerate(fitness):
        neighbor_idx = np.mod((i + np.arange(neighbor_size) - half_neighbor_size + len(fitness)),len(fitness))
        neighbor_fitness = fitness[neighbor_idx]
        neighbor_states = states[neighbor_idx]
        
        lb_updates = np.logical_and(neighbor_fitness > lb_fitness[i], neighbor_idx != i)
        lb_fitness[neighbor_idx[lb_updates]] = neighbor_fitness[lb_updates]
        lb_states[neighbor_idx[lb_updates]] = neighbor_states[lb_updates]

    particles_dict['pb_fitness'] = pb_fitness
    particles_dict['pb_states'] = pb_states
    particles_dict['lb_fitness'] = lb_fitness
    particles_dict['lb_states'] = lb_states

    return particles_dict


def get_gb(particles):
    pb_fitness = particles['pb_fitness']
    pb_states = particles['pb_states']

    max_idx = np.argmax(pb_fitness)
    return pb_states[max_idx], pb_fitness[max_idx]



def optimize_pso(tile_map):
    params = dict()
    params['population_size'] = 1000
    params['neighbor_size'] = 200

    params['min_epochs'] = 1000
    #params['max_epochs'] = 10000
    params['max_epochs'] = None
    params['window'] = 10
    #params['min_slope'] = 1E-6
    params['min_slope'] = None
    params['min_energy'] = 1.0

    params['pool'] = None

    params['C1'] = 1.59
    params['C2'] = 1.59
    params['C3'] = 1E-8
    params['dt'] = 1.0

    params['mutation_rate'] = 0.03

    params['dimensions'] = len(tile_map) * 3

    states = np.random.random(size=(params['population_size'], params['dimensions']))
    params['min_state'] = np.zeros(shape=states.shape)
    params['max_state'] = np.ones(shape=states.shape)
    v = np.random.random(size=states.shape) - 0.5

    pbest = states.copy()
    lbest = states.copy()

    fitness = np.full(shape=(params['population_size'],), fill_value=-float('inf'))
    pb_fitness = fitness.copy()
    lb_fitness = fitness.copy()

    particles = {
        'params': params,
        'states': states,
        'v': v,
        'fitness': fitness,
        'pb_states': pbest,
        'lb_states': lbest,
        'pb_fitness': pb_fitness,
        'lb_fitness': lb_fitness,
        'energy': 0.0
    }

    epochs = 0
    history = deque()
    while True:
        particles = fly(particles)
        particles = get_fitness(tile_map, particles)
        particles = evaluate(particles)
        _,gb_fitness = get_gb(particles)
        print(" - epoch({:4d}) :: {:0.6g}, Energy({:0.6g})".format(epochs, gb_fitness, particles['energy']))
        history.append(gb_fitness)
        if len(history) >= params['window']:
            history.popleft()
        epochs += 1
        if epochs >= params['min_epochs']:
            if params.get('max_epochs') is not None:
                if epochs >= params['max_epochs']:
                    break
            slope = (history[-1] - history[0]) / len(history)
            if params.get('min_slope') is not None:
                if slope <= params['min_slope']:
                    print("Reached min slope")
                    break
            if params.get('min_energy') is not None:
                if particles['energy'] <= params.get('min_energy'):
                    print("Reached min energy")
                    break

    return get_gb(particles), particles


def orientation_map(x):
    return (x % 4) * 90

def rotate(corners, idx):
    corners_c = corners.copy()
    if (idx % 4) == 1:
        corners_c[ 0, -1] = corners[ 0,  0]
        corners_c[ 0,  0] = corners[-1,  0]
        corners_c[-1,  0] = corners[-1, -1]
        corners_c[-1, -1] = corners[ 0, -1]
    elif (idx % 4) == 2:
        corners_c[ 0, -1] = corners[-1,  0]
        corners_c[ 0,  0] = corners[-1, -1]
        corners_c[-1,  0] = corners[ 0, -1]
        corners_c[-1, -1] = corners[ 0,  0]
    elif (idx % 4) == 3:
        corners_c[ 0, -1] = corners[-1, -1]
        corners_c[ 0,  0] = corners[ 0, -1]
        corners_c[-1,  0] = corners[ 0,  0]
        corners_c[-1, -1] = corners[-1,  0]
    return corners_c
def flip_h(corners):
    corners_c = corners.copy()
    corners_c[0,0],corners_c[-1,0] = corners_c[-1,0],corners_c[0, 0]
    corners_c[0,-1],corners_c[-1,-1] = corners_c[-1,-1],corners_c[0, -1]
    return corners_c

def flip_v(corners):
    corners_c = corners.copy()
    corners_c[0,0],corners_c[0,-1] = corners_c[0,-1],corners_c[0, 0]
    corners_c[-1,0],corners_c[-1,-1] = corners_c[-1,-1],corners_c[-1,0]
    return corners_c


def rebuild_tiles(tiles):
    
    # Establish orientation map for reference ( who cares )

    # Get unique tile IDs
    tile_id_set = set(tiles.keys())

    # Grab corners and assign orientations + neighbor tiles
    tile_map = dict()
    for tile_id, grid in tiles.items():
        edges = np.array([
            grid[:,0].flatten(),
            grid[:,-1].flatten(),
            grid[0,:].flatten(),
            grid[-1,:].flatten(),
        ])
        counts = [
            dict(Counter(edges[0])),
            dict(Counter(edges[1])),
            dict(Counter(edges[2])),
            dict(Counter(edges[3])),
        ]
        tile_map[tile_id] = dict()
        tile_map[tile_id]['corners'] = np.array([
            [grid[0,0], grid[0,-1]], [grid[-1,-1], grid[-1,0]]
        ])
        tile_map[tile_id]['edges'] = edges
        tile_map[tile_id]['edge_counts'] = counts
        tile_map[tile_id]['neighbors'] = tile_id_set.copy()
        tile_map[tile_id]['neighbors'].remove(tile_id)
        tile_map[tile_id]['orientations'] = set(range(4))
        tile_map[tile_id]['flips'] = {'h', 'v', 'n'}

    for tile_id, mapping in tile_map.items():
        print(tile_id, mapping['neighbors'])

    print("Reduce matchings")
    for left_tile_id, left_mapping in tile_map.items():
        invalid_mappings = set()
        for right_tile_id in left_mapping['neighbors']:
            if left_tile_id == right_tile_id:
                continue
            right_mapping = tile_map[right_tile_id]
            found = False
            for left_edges in left_mapping['edges']:
                for right_edges in right_mapping['edges']:
                    if np.all(left_edges == right_edges) or np.all(left_edges == np.flip(right_edges)):
                        found = True
                        print("Found: {} to {}".format(left_edges, right_edges))
                        break
                if found:
                    break
            if not found:
                invalid_mappings.add(right_tile_id)
            
        while len(invalid_mappings) > 0:
            right_tile_id = invalid_mappings.pop()
            tile_map[left_tile_id]['neighbors'].remove(right_tile_id)
            tile_map[right_tile_id]['neighbors'].remove(left_tile_id)


    for tile_id, mapping in tile_map.items():
        print(tile_id, mapping['neighbors'])

    assignment_list = optimize_pso(tile_map)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    parser.add_argument("--expected-layout", "-e", type=str, default=None)
    args = parser.parse_args()

    tiles = load_data(args.input_filename)

    final_image = rebuild_tiles(tiles)

    if args.expected_layout is not None:
        assert(os.path.exists(args.expected_layout))
        expected_layout = None
        with open(args.expected_layout, 'r') as ifile:
            expected_layout = ifile.read()
        print(expected_layout)
    


if __name__ == '__main__':
    main()