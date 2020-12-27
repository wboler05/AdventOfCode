#!/usr/bin/env python3

import argparse, os, sys
import re
from collections import deque
import numpy as np

from copy import deepcopy

from part1 import load_data, build_cards, get_deck_str

class HashSet(object):
    def __init__(self):
        self.hash_dict = dict()

    def _key(self, container):
        return np.sum(container)
    
    def add(self, container):
        container = np.array(container)
        key = self._key(container)
        if key not in self.hash_dict:
            self.hash_dict[key] = list()
        for c in self.hash_dict[key]:
            if np.all(c == container):
                return
        self.hash_dict[key].append(np.array(container))

    def __contains__(self, container):
        container = np.array(container)
        key = self._key(container)
        if key in self.hash_dict:
            for c in self.hash_dict[key]:
                if np.all(container == c):
                    return True
        return False


def play_game(player_1, player_2, game_number=1):
    memo = HashSet()

    print("-- Game {} --".format(game_number))

    round_num = 1
    while True:
        print("-- Round {} --".format(round_num))

        print("Player 1's deck: {}".format(get_deck_str(player_1)))
        print("Player 2's deck: {}".format(get_deck_str(player_2)))

        if player_1 in memo:
            return True
        if player_2 in memo:
            return True
        memo.add(player_1)
        memo.add(player_2)

        card1 = player_1.popleft()
        print("Player 1 plays: {}".format(card1))
        card2 = player_2.popleft()
        print("Player 2 plays: {}".format(card2))

        player_1_wins = card1 > card2

        if card1 <= len(player_1) and card2 <= len(player_2):
            print("Playing a sub-game to determine the winner...")
            player_1_wins = play_game(
                deque(list(player_1)[:card1]), 
                deque(list(player_2)[:card2]), 
                game_number + 1
            )
            print("...anyway, back to game {}".format(game_number))

        if player_1_wins:
            print("Player 1 wins the round {} of game {}!".format(round_num, game_number))
            player_1.append(card1)
            player_1.append(card2)
            if len(player_2) == 0:
                break
        else:
            print("Player 2 wins the round {} of game {}!".format(round_num, game_number))
            player_2.append(card2)
            player_2.append(card1)
            if len(player_1) == 0:
                break
        print()
        round_num += 1

    print("")

    if game_number != 1:
        if len(player_1) > 0:
            print("The winner of game {} is player 1!".format(game_number))
            return True
        else:
            print("The winnder of game {} is player 2!".format(game_number))
        

    print("== Post-game results ==")
    print("Player 1's deck: {}".format(get_deck_str(player_1)))
    print("Player 2's deck: {}".format(get_deck_str(player_2)))

    if len(player_1) > 0:
        print("Player 1 Wins!")
        mults = np.arange(len(player_1), 0, step=-1)
        val = np.sum(np.array(player_1) * mults)
        print("Mult = {}".format(val))
        return True
    else:
        print("Player 2 Wins!")
        mults = np.arange(len(player_2), 0, step=-1)
        val = np.sum(np.array(player_2) * mults)
        print("Mult = {}".format(val))
        return False



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    play_game(*build_cards(load_data(args.input_filename)))

if __name__ == '__main__':
    main()