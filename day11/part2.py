#!/usr/bin/env python3

import argparse, os, sys
import numpy as np

def print_chairs(grid):
  for row in grid:
    for col in row:
      print("{}".format(col), end="")
    print("\n")
  print("\n")

def get_chair_status(row, col, grid):
  if(row < 0 or row >= grid.shape[0]):
    return 'empty'
  if(col < 0 or col >= grid.shape[1]):
    return 'empty'

  if grid[row,col] == "#":
    return "occupied"
  else:
    return "empty"

def handle_chair_status(row, col, grid):
  occupied_count = 0
  empty_count = 0
  chair_status = get_chair_status(row, col, grid)

  if grid[row,col] == ".":
    return "."

  def get_first_chair(i, j, i_del, j_del, grid):
    while (i >= 0 and i < grid.shape[0] and j >= 0 and j < grid.shape[1]):
      if grid[i, j] == '.':
        pass
      else:
        return get_chair_status(i, j, grid)
      i += i_del
      j += j_del
    return "empty"


  adj_empty_count = 0
  
  # Up
  chair_status = get_first_chair(row-1, col, -1, 0, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  # Down
  chair_status = get_first_chair(row+1, col, 1, 0, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  # Left
  chair_status = get_first_chair(row, col-1, 0, -1, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  # Right
  chair_status = get_first_chair(row, col+1, 0, 1, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  # Diag Left Up
  chair_status = get_first_chair(row-1, col-1, -1, -1, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  # Diag Right Up
  chair_status = get_first_chair(row-1, col+1, -1, +1, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  # Diag Left Down
  chair_status = get_first_chair(row+1, col-1, 1, -1, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  # Diag Right Down
  chair_status = get_first_chair(row+1, col+1, 1, 1, grid)
  if chair_status == 'empty':
    empty_count += 1
  else:
    occupied_count += 1

  #print("Empty Count: {}\nOccupied Count: {}".format(empty_count, occupied_count))
  if adj_empty_count == 8:
    return "#"
  if empty_count == 8:
    return "#"
  elif occupied_count >= 5:
    return "L"
  else:
    return grid[row,col]


def process_chairs(grid):
  next_grid = grid.copy()
  for i,row in enumerate(grid):
    for j,chair in enumerate(row):
      next_grid[i,j] = handle_chair_status(i, j, grid)
  return next_grid

def count_occupied(grid):
  occupied_count = 0
  for row in grid:
    for chair in row:
      if chair == '#':
        occupied_count += 1
  return occupied_count

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("input_filename", type=str)
  args = parser.parse_args()

  data = None
  with open(args.input_filename, 'r') as ifile:
    data = ifile.read().split('\n')
    data = [chair for chair in np.array([list(row) for row in data if len(row) > 0])]
  print(data)
  data = np.array(data).astype(str)

  rules = {
    ".": "floor",
    "L": "empty",
    "#": "occupied",
  }

  grid = data.copy()
  #for z in range(6):
  while True:
    print_chairs(grid)
    new_grid = process_chairs(grid)
    if np.all(new_grid == grid):
      print("Occupied Count: {}".format(count_occupied(grid)))
      break
    else:
      grid = new_grid

