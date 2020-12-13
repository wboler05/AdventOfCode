#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import re

class Swaggy(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0

    def action(self, direction, value):
        if direction in {'N', 'S', 'E', 'W'}:
            self.shift(direction, value)
        elif direction in {'L', 'R'}:
            self.rotate(direction, value)
        elif direction in {'F'}:
            self.forward(value)
        else:
            print("WTF: {}{}".format(direction, value))

    def shift(self, direction, value):
        if direction == 'N':
            self.y += value
        elif direction == 'S':
            self.y -= value
        elif direction == 'E':
            self.x += value
        elif direction == 'W':
            self.x -= value

    def rotate(self, direction, value):
        if direction == 'L':
            self.direction += value
        elif direction == 'R':
            self.direction -= value
        self.direction = (self.direction+360) % 360

    def forward(self, value):
        if self.direction == 0: # East
            self.shift('E', value)
        elif self.direction == 90: # North
            self.shift('N', value)
        elif self.direction == 180: # West
            self.shift('W', value)
        elif self.direction == 270: # South
            self.shift('S', value)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", type=str)
    #parser.add_argument("--waypoint", "-w", nargs=2, type=int, default=(1,1))
    args = parser.parse_args()

    pattern = r"^(?P<direction>\w)(?P<digits>[\d]+)$"

    with open(args.input_filename, 'r') as ifile:
        data = ifile.read().split('\n')
        data = [d for d in data if len(d) > 0]
    
    direction_list = list()
    for d in data:
        m = re.search(pattern, d)
        if m is not None:
            direction = m.group("direction")
            value = int(m.group("digits"))
            direction_list.append({
                "direction":direction,
                "value":value
            })
    
    #for d in direction_list:
    #    print(d)

    boy = Swaggy()
    for d in direction_list:
        boy.action(d['direction'], d['value'])
        print("{}{}: {}, {}".format(d['direction'], d['value'],boy.x, boy.y))
    # Start point is 0,0
    distance = np.abs(boy.x) + np.abs(boy.y)
    print("Distance traveled: {}".format(distance))
