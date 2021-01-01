#!/usr/bin/env python3

import argparse, os, sys
import tqdm
import numpy as np
import re
from collections import Counter, deque

from multiprocessing import Pool
from itertools import repeat
from copy import deepcopy

from part1 import load_data, get_row_column, get_idx, \
    rotate, flip_edges, flip_h, flip_v, handle_rotation_flip, \
    compare_tiles_relative, reduce_tiles


def validate_assignment_map(tile_map, assignment_map, k):
    assert(assignment_map.shape == (k, k))
    found_set = set()
    for element in assignment_map.flatten():
        if isinstance(element, dict):
            if element['tile_id'] in found_set:
                return False
            else:
                found_set.add(element['tile_id'])
    return True


def build_potential_map(tile_map):

    tile_id_set = set(tile_map.keys())
    k = np.sqrt(len(tile_id_set)).astype(int)
    tile_dict = dict()
    for t in tile_id_set:
        rotation_flip_set = set()
        for r in {0, 1}:
            for f in {'v', 'h', 'b', 'n'}:
                rotation_flip_set.add((r, f))
        tile_dict[t] = rotation_flip_set
    
    potential_map = np.empty((k,k), dtype=object)
    for i in range(k):
        for j in range(k):
            potential_map[i,j] = tile_dict.copy()

    return potential_map

def check_potential_map_complete(potential_map):
    for i in range(potential_map.shape[0]):
        for j in range(potential_map.shape[1]):
            tile_dict = potential_map[i,j]
            if len(tile_dict) > 1 or len(tile_dict) == 0:
                return False
            if len(tile_dict[list(tile_dict.keys())[0]]) > 1:
                return False
    return True

def relax_single_tile_id(potential_map):
    # Relax by Tile_ID
    overall_change = False
    change = True
    while change:
        change = False
        for i in range(potential_map.shape[0]):
            for j in range(potential_map.shape[1]):
                tile_dict = potential_map[i,j]
                if len(tile_dict) == 1:
                    tile_id = list(potential_map[i,j].keys())[0]
                    # Remove tile ID From all other tiles
                    for m in range(potential_map.shape[0]):
                        for n in range(potential_map.shape[1]):
                            if i != m and j != n:
                                if tile_id in potential_map[m,n]:
                                    change = True
                                    overall_change = True
                                    potential_map[m,n].pop(tile_id)
    #print_potential_map(potential_map)
    return overall_change

def relax_potential_neighbors(tile_map, potential_map):
    k = np.sqrt(len(tile_map)).astype(int)

    overall_change = False
    change = True
    while change:
        change = False
        for i in range(potential_map.shape[0]):
            for j in range(potential_map.shape[1]):
                if len(potential_map[i,j]) == 1:
                    tile_id = list(potential_map[i,j].keys())[0]
                    allowed_neighbors = deepcopy(tile_map[tile_id]['neighbors'])

                    shifts = [
                        (i+1, j),
                        (i-1, j),
                        (i, j+1),
                        (i, j-1),
                    ]
                    for s in shifts:
                        if s[0] >= 0 and s[0] < k and s[1] >= 0 and s[1] < k:
                            actual_neighbors = set(potential_map[s[0], s[1]].keys())
                            ref = potential_map[s[0], s[1]].keys()
                            for n in actual_neighbors:
                                if n == tile_id:
                                    potential_map[s[0], s[1]].pop(n)
                                elif n not in allowed_neighbors:
                                    potential_map[s[0], s[1]].pop(n)
                                    change = True
                                    overall_change = True
    #print_potential_map(potential_map)
    return overall_change


def deeper_relax_potential_neighbors(tile_map, potential_map):
    k = np.sqrt(len(tile_map)).astype(int)

    overall_change = False
    change = True
    while change:
        change = False
        for i in range(potential_map.shape[0]):
            for j in range(potential_map.shape[1]):
                #potential_map(potential_map)
                valid_neighbors = set()
                for tile_id in potential_map[i,j].keys():
                    #tile_id = list(potential_map[i,j].keys())[0]
                    for s in tile_map[tile_id]['neighbors']:
                        valid_neighbors.add(s)
                    #valid_neighbors |= tile_map[tile_id]['neighbors']

                shifts = [
                    (i+1, j),
                    (i-1, j),
                    (i, j+1),
                    (i, j-1),
                ]
                for s in shifts:
                    if s[0] >= 0 and s[0] < k and s[1] >= 0 and s[1] < k:
                        actual_neighbors = set(potential_map[s[0], s[1]].keys())
                        for n in actual_neighbors:
                            if tile_id == n:
                                continue
                            if n not in valid_neighbors:
                                potential_map[s[0], s[1]].pop(n)
                                change = True
                                overall_change = True
                                #print_potential_map(potential_map)
    #print_potential_map(potential_map)
    return overall_change

def relax_rotations_and_flips(tile_map, potential_map):
    k = np.sqrt(len(tile_map)).astype(int)

    overall_change = False
    change = True
    while change:
        change = False
        # For each row, i
        for i in tqdm.tqdm(range(potential_map.shape[0])):
            # For each column, j
            for j in tqdm.tqdm(range(potential_map.shape[1])):
                # Establish the valid set
                valid_set = set()
                attempt_set = set()
                pmaps = deepcopy(potential_map[i,j])
                # For each potential tile
                for tile_id, rf_maps in pmaps.items():
                    #print(rf_maps)
                    # We're going to rotate and flip each edge
                    edges = tile_map[tile_id]['edges']
                    for rotation, orientation in rf_maps:
                        # Remember which ones we've tried already
                        attempt_set.add((rotation, orientation))
                        # We'll have a check for at least one good match
                        is_this_good_setup = True
                        # Let's apply our flips and rotations
                        c_edges = handle_rotation_flip(edges, rotation, orientation)

                        # Time to check the neighbors
                        shifts = [
                            (i+1, j, 'bottom'),
                            (i-1, j, 'top'),
                            (i, j+1, 'right'),
                            (i, j-1, 'left'),
                        ]
                        # A shift is a neighbor position
                        for s in shifts:
                            # Ensure its within bounds, at least 0 or at most k-1
                            if s[0] >= 0 and s[0] < k and s[1] >= 0 and s[1] < k:
                                # Find at least one friendly neighbor
                                my_tile_has_no_friends = True
                                ref = potential_map[s[0],s[1]].keys()
                                #print(" Neighbor Keys: {}".format(ref))
                                for n_tile_id, n_rf_maps in potential_map[s[0], s[1]].items():
                                    if n_tile_id == tile_id:
                                        continue
                                    n_edges  = tile_map[n_tile_id]['edges']
                                    for n_rotation, n_orientation in n_rf_maps:
                                        nc_edges = handle_rotation_flip(n_edges, n_rotation, n_orientation)
                                        # Check to see if the expected edges match
                                        if compare_tiles_relative(c_edges, nc_edges, s[2]):
                                            # If found, we're happy and we no longer need to check this shift
                                            my_tile_has_no_friends = False
                                            break
                                    # We found a friend (double negative)
                                    if not my_tile_has_no_friends:
                                        break
                                # If we couldn't match this shift, then none else matters
                                if my_tile_has_no_friends:
                                    is_this_good_setup = False
                                    break
                            # We've exhausted all neighbors for this index, so no need to check others
                            if not is_this_good_setup:
                                break
                        # We only add this setup if we have at least one good match
                        if is_this_good_setup:
                            valid_set.add((rotation, orientation))
                    if len(valid_set) != len(attempt_set):
                        change = True
                        overall_change = True
                    if len(valid_set) == 0:
                        potential_map[i,j].pop(tile_id)
                    else:
                        potential_map[i,j][tile_id] = deepcopy(valid_set)
                    #print_potential_map(potential_map)
        break

    #print_potential_map(potential_map)
    return overall_change
                                

def relax_lonely(potential_map):
    change = False
    potential_locations = dict()
    for i in range(potential_map.shape[0]):
        for j in range(potential_map.shape[1]):
            for tile_id in potential_map[i,j].keys():
                if tile_id not in potential_locations:
                    potential_locations[tile_id] = list()
                potential_locations[tile_id].append((i,j))

    lonely_tiles = dict()
    for tile_id, locs in potential_locations.items():
        if len(locs) == 1:
            lonely_tiles[tile_id] = locs[0]

    for tile_id, loc in lonely_tiles.items():
        available_tiles = set(potential_map[loc[0], loc[1]].keys())
        for a in available_tiles:
            if a != tile_id:
                potential_map[loc[0], loc[1]].pop(a)
                change = True

    #print_potential_map(potential_map)
    return change



def validate_potential_map(potential_map):
    '''
    If any sets are empty, this mapping is a failure
    '''
    hard_assignments = set()
    for i in range(potential_map.shape[0]):
        for j in range(potential_map.shape[1]):
            if len(potential_map[i,j]) == 0:
                print(" - Invalid map")
                #print_potential_map(potential_map)
                return False
            if len(potential_map[i,j]) == 1:
                tile_id = list(potential_map[i,j].keys())[0]
                if tile_id in hard_assignments:
                    print(" - Invalid map")
                    #print_potential_map(potential_map)
                    return False
                else:
                    hard_assignments.add(tile_id)
    return True

def print_potential_map(potential_map):
    print("** *")
    print("*** ** *")
    print("**** *** ** *")
    print("***** **** *** ** *")
    for i in range(potential_map.shape[0]):
        for j in range(potential_map.shape[1]):
            print(i, j, 
                { k:len(c) for k,c in potential_map[i,j].items() }
            )
    print("***** **** *** ** *")
    print("**** *** ** *")
    print("*** ** *")
    print("** *")


def relax_constraints(tile_map, assignment_map, potential_map):

    change = True
    while change:

        max_states = 0
        max_tiles = 0
        for i in range(potential_map.shape[0]):
            for j in range(potential_map.shape[0]):
                max_tiles = max(len(potential_map[i,j].keys()), max_tiles)
                for tile_id, mappings in potential_map[i,j].items():
                    max_states = max(len(mappings), max_states)
        print("Max states this go: {}".format(max_states * max_tiles))
        print(" Tile Counts: {}".format(max_tiles))
        print(" States Counts: {}".format(max_states))
        print_potential_map(potential_map)


        change = False
        change |= relax_single_tile_id(potential_map)
            
        if not validate_potential_map(potential_map):
            return False

        change |= relax_potential_neighbors(tile_map, potential_map)
        if not validate_potential_map(potential_map):
            return False

        change |= deeper_relax_potential_neighbors(tile_map, potential_map)

        change |= relax_lonely(potential_map)
        if not validate_potential_map(potential_map):
            return False
        
        change |= relax_rotations_and_flips(tile_map, potential_map)
        if not validate_potential_map(potential_map):
            return False

        if not change:
            if not check_potential_map_complete(potential_map):
                change = kill_something(potential_map)
        if check_potential_map_complete(potential_map):
            break

    #if not check_potential_map_complete(potential_map):
    #    potential_map = dfs(potential_map, 0, 0, np.sqrt(len(tile_map)).astype(int))

    # Evaluate sets
    return check_potential_map_complete(potential_map)


'''(((***)))'''

'''(((***)))'''

def recursive_check_neighbors(tile_map, master_arrangement, neighbor_dict, parent_chain, frontier, max_depth):

    valid_chains = list()

    depth = len(parent_chain)
    if depth == max_depth:
        return [ parent_chain ]

    elif depth == 0:
        for tile_id in tqdm.tqdm(frontier):
            edges = deepcopy(tile_map[tile_id]['edges'])
            new_frontier = set(neighbor_dict[tile_id])
            for arrangement in master_arrangement:
                r_edges = handle_rotation_flip(edges, arrangement['rotation'], arrangement['flip'])
                new_parent_chain = list()
                new_parent_chain.append({
                    'tile_id':tile_id,
                    'arrangement':arrangement,
                    'edges':r_edges,
                })

                chains = recursive_check_neighbors(
                    tile_map, 
                    master_arrangement, 
                    neighbor_dict, 
                    new_parent_chain, new_frontier, 
                    max_depth
                )

                for c in chains:
                    valid_chains.append(c)

    else:

        parent = parent_chain[-1]

        for tile_id in frontier:
            # Check if already in parent chain:
            parent_set = set([p['tile_id'] for p in parent_chain])
            if tile_id in parent_set:
                continue
            new_frontier = set(neighbor_dict[tile_id]) - parent_set

            edges = deepcopy(tile_map[tile_id]['edges'])

            for arrangement in master_arrangement:

                r_edges = handle_rotation_flip(edges, arrangement['rotation'], arrangement['flip'])
                if compare_tiles_relative(parent['edges'], r_edges, 'bottom'):
                    new_parent_chain = deepcopy(parent_chain)
                    new_parent_chain.append({
                        'tile_id': tile_id,
                        'arrangement': arrangement,
                        'edges': r_edges,
                    })
                    chains = recursive_check_neighbors(
                        tile_map, 
                        master_arrangement, 
                        neighbor_dict, 
                        new_parent_chain, 
                        new_frontier, 
                        max_depth
                    )
                    for c in chains:
                        valid_chains.append(c)

    return valid_chains


def generate_adjacency_chains_dict(tile_map):

    k = np.sqrt(len(tile_map)).astype(int)

    neighbor_dict = dict()

    # Generate arrangment of rotations and flips
    #rotation_set = {0, 1}
    #flip_set = {'n', 'h', 'v'}
    rotation_set = {0, 1, 2, 3}
    flip_set = {'n', 'h', 'v'}
    master_arrangement = list()
    for r in rotation_set:
        for f in flip_set:
            master_arrangement.append({
                'rotation':r,
                'flip':f,
            })

    for tile_id, mapping in tile_map.items():
        if tile_id not in neighbor_dict:
            neighbor_dict[tile_id] = deepcopy(mapping['neighbors'])

    chain_paths = recursive_check_neighbors(tile_map, master_arrangement, neighbor_dict, list(), set(tile_map.keys()), k)
    return chain_paths
    
def align_chains(tile_map, chain_paths):

    print("Total chains generated: {}".format(len(chain_paths)))

    print(" - Generating Edge Lists O(N)")

    left_edges = list()
    right_edges = list()
    for chain in tqdm.tqdm(chain_paths):
        left_edge = list()
        right_edge = list()
        for link in chain:
            left_edge.extend(list(link['edges'][2]))
            right_edge.extend(list(link['edges'][3]))
        left_edges.append(np.array(left_edge))
        right_edges.append(np.array(right_edge))

    print(" - Generating edge pairs O(N^2)")

    pairs = dict()
    for i in tqdm.tqdm(range(len(chain_paths))):
        for j in range(len(chain_paths)):
            if i == j:
                continue
            left_set = set([c['tile_id'] for c in chain_paths[i]])
            right_set = set([c['tile_id'] for c in chain_paths[j]])
            if len(left_set & right_set) > 0:
                continue
            if np.all(right_edges[i] == left_edges[j]):
                pairs[i] = j

    print(" -- Generated pairs: {}".format(len(pairs)))
    print(" - Building potential image assignments")

    k = np.sqrt(len(tile_map)).astype(int)
    potential_images = list()
    for left_idx, right_idx in tqdm.tqdm(pairs.items()):
        potential_image_assignment = [ left_idx, right_idx ]
        cache = right_idx
        while cache in pairs and len(potential_image_assignment) < k:
            potential_image_assignment.append(pairs[cache])
            cache = pairs[cache]
        if len(potential_image_assignment) == k:
            potential_images.append(potential_image_assignment)

    print(" -- Built image assignments: {}".format(len(potential_images)))
    print(" - Compiling images")

    images = list()
    for potential_image in tqdm.tqdm(potential_images):
        image = list()
        tile_id_set = set()
        for left_idx in potential_image:
            chain = chain_paths[left_idx]
            image.append(deepcopy(chain))
            tile_id_set |= { c['tile_id'] for c in chain }
        if len(tile_id_set) == len(tile_map):
            images.append(image)

    print(" - Total images found: {}".format(len(images)))

    if len(images) >= 1:
        # Multiple may be found, so just return one of them
        return images[0]
    else:
        # Return an empty list in case none found
        return list()


def get_corners(final_image):
    k = len(final_image)
    assert(k > 0)
    corners = [
        final_image[0][0]['tile_id'],
        final_image[0][k-1]['tile_id'],
        final_image[k-1][0]['tile_id'],
        final_image[k-1][k-1]['tile_id'],
    ]
    return np.array(corners).astype(int)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    parser.add_argument("--expected-layout", "-e", type=str, default=None)
    args = parser.parse_args()

    tiles = load_data(args.input_filename)

    print("Reducing Tiles")
    tile_map = reduce_tiles(tiles)

    print("Generating adjacency chains")
    chain_paths = generate_adjacency_chains_dict(tile_map)

    print("Aligning chains")
    final_image = align_chains(tile_map, chain_paths)
    corners = get_corners(final_image)
    mult = 1
    for c in corners:
        mult *= c

    print(" Corners: {}".format(corners))
    print("  -- Product: {}".format(mult))
    print("Complete")
    
    


if __name__ == '__main__':
    main()