#!/usr/bin/env python3

import argparse, os, sys
import tqdm
import numpy as np
import re
from collections import Counter, deque

from multiprocessing import Pool
from itertools import repeat
from copy import deepcopy

def load_data(input_filename):
    '''
    Loads data into tile_dict from filename

    @param input_filename : Path to file to open(,'r')
    @return tile_dict : Dictionary of tiles[tile_id] = np.matrix(grid)
    '''
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
    '''
    Returns tuple of row,col based on index and K

    @param idx : integer from 0 to N of k**2 values, row to col
    @param k : np.sqrt(N) as square edge size
    @return (row,col) : Row = idx / k, col = idx % k
    '''
    row = np.floor(idx / k).astype(int)
    col = idx % k
    return row, col

def get_idx(row, col, k):
    return row * k + col


def rotate(edges, idx):
    '''
    Counter clockwise rotation in 90 deg increments

    @param edges : np.matrix of border edges : Top, Bottom, Left, Right
    @param idx : Rotation index by 90 deg CCW shifts
    @return edges_c : np.matrix of rotated edges
    '''
    edges_c = edges.copy()
    if (idx % 4) == 1:
        # 1 shift CCW
        # Top -> Left and flipped
        edges_c[2] = np.flip(edges[0])
        # Left -> Bottom
        edges_c[1] = edges[2]
        # Bottom -> Right and flipped
        edges_c[3] = np.flip(edges[1])
        # Right -> Top
        edges_c[0] = edges[3]

    elif (idx % 4) == 2:
        # 2 shifts CCW
        # Top -> Bottom and flip
        edges_c[1] = np.flip(edges[0])
        # Left -> Right and flip
        edges_c[3] = np.flip(edges[2])
        # Bottom -> Top and flip
        edges_c[0] = np.flip(edges[1])
        # Right -> Left and flip
        edges_c[2] = np.flip(edges[3])

    elif (idx % 4) == 3:
        # 3 shifts CCW
        # Top -> Right
        edges_c[3] = edges[0]
        # Right -> Bottom and flip
        edges_c[1] = np.flip(edges[3])
        # Bottom -> Left
        edges_c[2] = edges[1]
        # Left -> Top and flip
        edges_c[0] = np.flip(edges[2])

    return edges_c

def flip_h(edges):
    '''
    Flip edges horizontally from left to right

    @param edges : np.matrix of border edges : Top, Bottom, Left, Right
    @return edges_c : np.matrix of horizontally flipped edges
    '''
    edges_c = edges.copy()
    # Flip Top
    edges_c[0] = np.flip(edges[0])
    # Flip Bottom
    edges_c[1] = np.flip(edges[1])
    # Swap Right to Left
    edges_c[2] = edges[3]
    # Swap Left to Right
    edges_c[3] = edges[2]
    return edges_c

def flip_v(edges):
    '''
    Flip edges vertically from top to bottom

    @param edges : np.matrix of border edges : Top, Bottom, Left, Right
    @return edges_c : np.matrix of vertically flipped edges
    '''
    edges_c = edges.copy()
    # Swap Bottom to Top
    edges_c[0] = edges[1]
    # Swap Top to Bottom
    edges_c[1] = edges[0]
    # Flip Left
    edges_c[2] = np.flip(edges[2])
    # Flip Right
    edges_c[3] = np.flip(edges[3])
    return edges_c

def flip_edges(edges, orientation):
    '''
    Handle flipping of edges based on orientation

    @param edges : np.matrix of border edges : Top, Bottom, Left, Right    
    @param orientation : Type of flip as character in set {'h': horiz, 'v': vert, 'b': both/transpose, 'n': None}
    @return edges_c : np.matrix of flipped edges
    '''
    if orientation == 'h':
        return flip_h(edges)
    elif orientation == 'v':
        return flip_v(edges)
    elif orientation == 'b':
        return flip_v(flip_h(edges))
    else:
        return edges.copy()

def handle_rotation_flip(edges, rotation, orientation):
    edges_c = rotate(edges, rotation)
    return flip_edges(edges_c, orientation)

def compare_tiles(tile_dict_a:dict, tile_dict_b:dict, b_relative_position:tuple):
    '''
    Compare two tiles placed next to each other

    @param tile_dict_a : Dictionary containing edges, rotation, and flip
    @param tile_dict_b : Dictionary containing edges, rotation, adn flip
    @param b_relative_position : Tuple of (row, col) b's relative position a -> b
    '''
    if b_relative_position[0] == b_relative_position[1]:
        raise Exception("Error, relative position must be {-1, 0, 1} and not equal")
    if np.all([b in {-1, 0, 1} for b in b_relative_position]):
        raise Exception("Error, relative position must be {-1, 0, 1} and not equal")

    a_edges = tile_dict_a['edges']
    a_edges = rotate(a_edges, tile_dict_a['orientation'])
    a_edges = flip_edges(a_edges, tile_dict_a['flip'])

    b_edges = tile_dict_b['edges']
    b_edges = rotate(b_edges, tile_dict_b['orientation'])
    b_edges = flip_edges(b_edges, tile_dict_b['flip'])

    #Above
    if b_relative_position[0] == 1:
        return np.all(a_edges[0] == b_edges[1])
    #Below
    elif b_relative_position[0] == -1:
        return np.all(a_edges[1] == b_edges[0])
    #Left
    elif b_relative_position[1] == -1:
        return np.all(a_edges[2] == b_edges[3])
    #Right
    elif b_relative_position[1] == 1:
        return np.all(a_edges[3] == b_edges[2])

    
def compare_tiles_relative(a_edges, b_edges, relation):
    if relation == 'top':
        return np.all(a_edges[0] == b_edges[1])
    elif relation == 'bottom':
        return np.all(a_edges[1] == b_edges[0])
    elif relation == 'left':
        return np.all(a_edges[2] == b_edges[3])
    elif relation == 'right':
        return np.all(a_edges[3] == b_edges[2])
    else:
        raise Exception("I don't know this relation: {}".format(relation))


def reduce_tiles(tiles):
    
    # Establish orientation map for reference ( who cares )

    # Get unique tile IDs
    tile_id_set = set(tiles.keys())

    # Grab corners and assign orientations + neighbor tiles
    tile_map = dict()
    for tile_id, grid in tiles.items():
        edges = np.array([
            grid[0,:].flatten(),    # Top Row
            grid[-1,:].flatten(),   # Bottom Row
            grid[:,0].flatten(),    # Left Column
            grid[:,-1].flatten(),   # Right Column
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
        tile_map[tile_id]['orientations'] = { 0, 1 }
        tile_map[tile_id]['flips'] = {'h', 'v', 'n', 'b'}

    #for tile_id, mapping in tile_map.items():
    #    print(tile_id, mapping['neighbors'])

    # Do a simple check to reduce the amount of flipping and nonsense
    print("Reduce matchings")
    for left_tile_id, left_mapping in tqdm.tqdm(tile_map.items()):
        invalid_mappings = set()
        for right_tile_id in left_mapping['neighbors']:
            if left_tile_id == right_tile_id:
                continue
            right_mapping = tile_map[right_tile_id]
            found = False
            for left_edge in left_mapping['edges']:
                for right_edge in right_mapping['edges']:
                    if np.all(left_edge == right_edge) or np.all(left_edge == np.flip(right_edge)):
                        found = True
                        #print("Found: {} to {}".format(left_edges, right_edges))
                        break
                if found:
                    break
            if not found:
                invalid_mappings.add(right_tile_id)
            
        while len(invalid_mappings) > 0:
            right_tile_id = invalid_mappings.pop()
            tile_map[left_tile_id]['neighbors'].remove(right_tile_id)
            tile_map[right_tile_id]['neighbors'].remove(left_tile_id)

    return tile_map


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


def assign_tile(assignment_map, assignment_stack, row, col, frontier):
    tile_id = frontier.pop()
    print(" - Assign {:5d} to ({:3d},{:3d})".format(tile_id, row, col))
    assignment_map[row, col] = {
        'tile_id': tile_id, 
        'frontier': frontier,
    }
    assignment_stack.append((row, col))
    return tile_id

def pop_stack(tile_map, assignment_map, assignment_stack, k):
    row, col = assignment_stack.pop()
    m = assignment_map[row, col]
    print(" - Pop {:5d} to ({:3d},{:3d})".format(m['tile_id'], row, col))
    while len(m['frontier']) > 0:
        if recurse_assign_map(tile_map, assignment_map, assignment_stack, row, col, m['frontier'], k):
            return True
    assignment_map[row, col]['tile_id'] = -1
    return False

def print_assignment_map(assignment_map):
    print("**** **** **** **** ****")
    for i in range(assignment_map.shape[0]):
        for j in range(assignment_map.shape[1]):
            r = assignment_map[i,j]
            if isinstance(r, dict):
                r = r['tile_id']
            print("\'{:5d}\'".format(r), end=' ')
        print("")
    print("**** **** **** **** ****\n")


def recurse_assign_map(tile_map, assignment_map, assignment_stack, row, col, frontier, k):

    tile_id = assign_tile(assignment_map, assignment_stack, row, col, frontier)

    print_assignment_map(assignment_map)    

    neighbor_set = tile_map[tile_id]['neighbors']
    print("Available Neighbors: {}".format(neighbor_set))
    # TODO Final sets will contain edges, rotation + flip

    if not validate_assignment_map(tile_map, assignment_map, k):
        return pop_stack(tile_map, assignment_map, assignment_stack, k)

    next_row = row + 1
    if next_row >= k:
        next_row = None
    next_col = col + 1
    if next_col >= k:
        next_col = None

    if not next_row and not next_col:
        return True
    if not next_row:
        return recurse_assign_map(tile_map, assignment_map, assignment_stack, row, next_col, neighbor_set.copy(), k)
    elif not next_col:
        return recurse_assign_map(tile_map, assignment_map, assignment_stack, next_row, col, neighbor_set.copy(), k)
    else:
        success = recurse_assign_map(tile_map, assignment_map, assignment_stack, next_row, col, neighbor_set.copy(), k)
        if success:
            return recurse_assign_map(tile_map, assignment_map, assignment_stack, row, next_col, neighbor_set.copy(), k)
        else:
            return pop_stack(tile_map, assignment_map, assignment_stack, k)


def calculate_final_image(tile_map):

    print("\n*************swag**************")
    print("*   Final Image Calculation   *")
    print("**swag*******************swag**\n")

    k = np.sqrt(len(tile_map)).astype(int)

    assignment_map = None
    # Do a simple check to reduce the total position checks
    assignment_map = np.full((k,k), -1, dtype=object)
    assignment_stack = deque()
    frontier = set(tile_map.keys())
    recurse_assign_map(tile_map, assignment_map, assignment_stack, 0, 0, frontier, k)

    print("\nFinal Image:: \n")
    print_assignment_map(assignment_map)

    return assignment_map


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

'''
def dfs(potential_map, row, col, k):

    if row >= k:
        return None
    if col >= k:
        return None

    frontier = set()
    visited = set()
    cache = deepcopy(potential_map)
    for trace_id, mapping:
        for m in mapping:
            frontier.add((trace_id, m))
    while len(frontier) > 0:
        trace_id, mapping = frontier.pop()
        cache[row, col] = {trace_id: {mapping,}}
        down_cache = dfs(cache, row+1, col, k)
        right_cache = dfs(cache, row, col+1, k)
        
        down_is_valid = validate_potential_map(down_cache)
        right_is_valid = validate_potential_map(right_cache)
'''

                


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

def kill_something(potential_map):
    for i in range(potential_map.shape[0]):
        for j in range(potential_map.shape[1]):
            if len(potential_map[i,j]) > 0:
                tile_id = list(potential_map[i,j].keys())[0]
                if len(potential_map[i,j][tile_id]) > 0:
                    potential_map[i,j][tile_id].pop()
                    return True
    return False


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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    parser.add_argument("--expected-layout", "-e", type=str, default=None)
    args = parser.parse_args()

    tiles = load_data(args.input_filename)

    tile_map = reduce_tiles(tiles)

    potential_map = build_potential_map(tile_map)

    assert(not check_potential_map_complete(potential_map))
    
    k = np.sqrt(len(tile_map.keys())).astype(int)
    
    for root_tile_id in tile_map.keys():
        assignment_map = np.full((k,k), -1, dtype=object)
        cache_map = deepcopy(potential_map)
        remove_keys = set(tile_map.keys())
        remove_keys.remove(root_tile_id)
        for r in remove_keys:
            cache_map[0,0].pop(r)
        print("Root Tile ID: {}".format(root_tile_id))
        if root_tile_id == 1951:
            print("Matched ya son!")
        if relax_constraints(tile_map, assignment_map, cache_map):
            print("Lucky you!")
            break
        if root_tile_id == 1951:
            print(" ... What did you do??")


    corners = list()
    corners.append(list(cache_map[0,0].keys())[0])
    corners.append(list(cache_map[0,k-1].keys())[0])
    corners.append(list(cache_map[k-1,0].keys())[0])
    corners.append(list(cache_map[k-1,k-1].keys())[0])
    print(" Corners: {}".format(corners))
    print("  -- Product: {}".format(np.dot(corners, corners)))
    print("Complete")
    
    sys.exit()

    for tile_id, mapping in tile_map.items():
        print(tile_id, mapping['neighbors'])

    final_image = calculate_final_image(tile_map)

    if args.expected_layout is not None:
        assert(os.path.exists(args.expected_layout))
        expected_layout = None
        with open(args.expected_layout, 'r') as ifile:
            expected_layout = ifile.read()
        print(expected_layout)
    


if __name__ == '__main__':
    main()