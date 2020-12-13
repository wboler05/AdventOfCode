#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import re

class ShipWaypoint(object):
    def __init__(self, x=0, y=0, way_x=1, way_y=1):
        self.start_point = (x,y)
        self.x = x
        self.y = y
        self.way_x = way_x
        self.way_y = way_y

    def action(self, direction, value):
        if direction in {'N', 'S', 'E', 'W'}:
            self.translate_waypoint(direction, value)
        elif direction in {'L', 'R'}:
            self.rotate_waypoint_about(direction, value)
        elif direction in {'F'}:
            self.move_towards_waypoint(value)
        else:
            print("No known action: {}{}".format(direction, value))

    def translate_waypoint(self, direction, value):
        if direction == 'N':
            self.way_y += value
        elif direction == 'S':
            self.way_y -= value
        elif direction == 'E':
            self.way_x += value
        elif direction == 'W':
            self.way_x -= value

    def rotate_waypoint_about(self, direction, value):
        ship_dir = 180. * np.arctan2(self.way_y, self.way_x) / np.pi
        new_dir = 0.
        if direction == 'R':
            new_dir = np.mod(ship_dir - value + 360, 360)
        elif direction == 'L':
            new_dir = np.mod(ship_dir + value + 360, 360)
        new_dir *= (np.pi / 180.)
        mag = np.sqrt(self.way_x**2 + self.way_y**2)
        self.way_x = np.round(mag * np.cos(new_dir)).astype(int)
        self.way_y = np.round(mag * np.sin(new_dir)).astype(int)

    def move_towards_waypoint(self, value):
        vx = self.way_x * value
        vy = self.way_y * value
        self.x += vy
        self.y += vx



    def manhatten_distance(self):
        return np.abs(self.x - self.start_point[0]) + np.abs(self.y - self.start_point[1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", type=str)
    parser.add_argument("--waypoint", "-w", nargs=2, type=int, default=(1,1))
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

    ship = ShipWaypoint(0, 0, args.waypoint[0], args.waypoint[1])
    for d in direction_list:
        ship.action(d['direction'], d['value'])
        print("{}{}: X({}), Y({}), WayX({}), WayY({})".format(
            d['direction'], d['value'],ship.x, ship.y, ship.way_x, ship.way_y
        ))
    print("Distance traveled: {}".format(ship.manhatten_distance()))
