#!/usr/bin/env python3

import argparse, os, sys

from part1 import get_seat_ids

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input_filename', type=str)
  parser.add_argument('--columns', '-c', default=8)
  parser.add_argument('--rows', '-r', default=128)
  parser.add_argument('--verbose', '-v', action='store_true')

  args = parser.parse_args()

  seat_id_info = get_seat_ids(args.input_filename, args.rows, args.columns, args.verbose)

  max_seat_id = max([v['seat_id'] for v in seat_id_info.values()])
  print("Max Seat ID: {}".format(max_seat_id))

  seat_ids = sorted([v['seat_id'] for v in seat_id_info.values()])
  for i in range(0, len(seat_ids)-1):
    s0 = seat_ids[i]
    s1 = seat_ids[i+1]
    delta = s1-s0
    if delta != 1:
      print(" - Delta({}), SeatID0({}), SeatID1({})".format(delta, s0, s1))



if __name__ == '__main__':
  main()
