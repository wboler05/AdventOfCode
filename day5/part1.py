#!/usr/bin/env python3

import argparse, os, sys

def recurse(msg, max_val, lower_key, verbose=False):

  #print("Recursing through msg: {}".format(msg))

  l_row = 0
  r_row = max_val

  cache = msg
  while (len(cache) > 0):
    #print("Cache: {}, Left: {}, Right: {}".format(cache, l_row, r_row))
    first = cache[0]
    if len(cache) > 1:
      cache = cache[1:]
    else:
      cache = ""
    m = int((r_row - l_row)/2)
    if first.lower() == lower_key:
      r_row -= m
    else:
      l_row += m

  return l_row


def calc_seat_id(row, column, total_columns):
  return (row * total_columns) + column

def extract_info(msg, total_rows, total_columns):

  fb = msg[0:-3]
  lr = msg[-3:]

  row = recurse(fb, total_rows, 'f')
  column = recurse(lr, total_columns, 'l')
  seat_id = calc_seat_id(row, column, total_columns)

  return row, column, seat_id


def get_seat_ids(input_filename, total_rows, total_columns, verbose):
  print("Input File: {}".format(input_filename))
  print("Rows: {}".format(total_rows))
  print("Columns: {}".format(total_columns))
  print("Verbose: {}".format(verbose))

  assert(os.path.exists(input_filename))
  data = None
  with open(input_filename, 'r') as ifile:
    data = ifile.read().split('\n')[:-1]
  assert(data is not None)
 
  print("Data length: {}".format(len(data)))
 
  if verbose:
    print("Show me the data")
    for d in data:
      print(d)
    print("Data print complete")

  print("Parsing data")
  seat_info = dict()
  for d in data:
    if len(d) == 0:
      continue
    #print("Extracting {}".format(d))
    row, column, seat_id = extract_info(d, total_rows, total_columns)
    if verbose:
      print(" - {:10s}: Row({:3d}), Column({:1d}), Seat ID({:4d})".format(
        d, row, column, seat_id
      ))
    seat_info[d] = {
      'row': row, 'column': column, 'seat_id': seat_id
    }

  return seat_info


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('input_filename')
  parser.add_argument('--rows', '-r', type=int, default=128)
  parser.add_argument('--columns', '-c', type=int, default=8)
  parser.add_argument('--verbose', '-v', action='store_true')

  args = parser.parse_args()
  
  seat_info = get_seat_ids(args.input_filename, args.rows, args.columns, args.verbose)
  
  max_seat_id = max([v['seat_id'] for v in seat_info.values()])
  print("Max Seat ID: {}".format(max_seat_id))

  

if __name__ == '__main__':
  main()  
