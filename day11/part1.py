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
  assert(row >= 0 and row < grid.shape[0])
  assert(col >= 0 and col < grid.shape[1])

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
  
  for i in range(row-1, row+2):
    for j in range(col-1, col+2):
      if i >= 0 and j >= 0 and i < grid.shape[0] and j < grid.shape[1]:
        #print("{}".format(grid[i,j]), end="")
        if i == row and j == col:
          #print("{}".format(grid[i,j]), end="")
          continue
        if get_chair_status(i, j, grid) == 'empty':
          empty_count += 1
        else:
          occupied_count += 1
      else:
        empty_count += 1
    #print("\n")
  #print("Empty Count: {}\nOccupied Count: {}".format(empty_count, occupied_count))
  if empty_count == 8:
    return "#"
  elif occupied_count >= 4:
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

