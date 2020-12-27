#!/usr/bin/env python3

import argparse, os, sys
import re
from collections import deque
import numpy as np

def load_data(input_filename):

    data = None
    with open(input_filename, 'r') as ifile:
        data = [d for d in ifile.read().split('\n\n') if len(d) > 0]
    
    player_cards = dict()
    for d in data:
        rows = [i for i in d.split('\n') if len(i) > 0]
        pattern = r"^(?:[Player\s]*)(?P<player_num>[\d]*)"
        m = re.search(pattern, rows[0])
        if m:
            player_num = int(m.group('player_num'))
            player_cards[player_num] = \
                np.array(rows[1:], dtype=int)
        else:
            raise Exception("Yeah, what? {}".format(rows[0]))
    return player_cards


def play_game(player_cards):

    player_1, player_2 = deque(), deque()

    for card in player_cards[1]:
        player_1.append(card)

    for card in player_cards[2]:
        player_2.append(card)

    def get_deck(deck):
        s = ""
        for i,d in enumerate(deck):
            s += "{}".format(d)
            if i != len(deck)-1:
                s += ", "
        return s

    round = 1
    while True:
        print("-- Round {} --".format(round))

        print("Player 1's deck: {}".format(get_deck(player_1)))
        print("Player 2's deck: {}".format(get_deck(player_2)))

        card1 = player_1.popleft()
        print("Player 1 plays: {}".format(card1))
        card2 = player_2.popleft()
        print("Player 2 plays: {}".format(card2))

        if card1 > card2:
            print("Player 1 wins the round!")
            player_1.append(card1)
            player_1.append(card2)
            if len(player_2) == 0:
                break
        elif card1 < card2:
            print("Player 2 wins the round!")
            player_2.append(card2)
            player_2.append(card1)
            if len(player_1) == 0:
                break
        print()
        round += 1

    print("== Post-game results ==")
    print("Player 1's deck: {}".format(get_deck(player_1)))
    print("Player 2's deck: {}".format(get_deck(player_2)))

    if len(player_1) > 0:
        print("Player 1 Wins!")
        mults = np.arange(len(player_1), 0, step=-1)
        val = np.sum(np.array(player_1) * mults)
        print("Mult = {}".format(val))
    else:
        print("Player 2 Wins!")
        mults = np.arange(len(player_2), 0, step=-1)
        val = np.sum(np.array(player_2) * mults)
        print("Mult = {}".format(val))

    return



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    player_cards = load_data(args.input_filename)
    play_game(player_cards)

if __name__ == '__main__':
    main()