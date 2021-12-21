from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


def get_total(c):
    total = 0
    for i in range(3):
        next = c + i
        if next > 100:
            next -= 100
        total += next
    return total


def main(inp, is_real):
    players = [int(p.split(': ')[1]) for p in inp.strip().split('\n')]
    pts = [0, 0]
    c = 1
    turn = 0
    throws = 0
    while all([p < 1000 for p in pts]):
        total = get_total(c)
        c += 3
        if c > 100:
            c -= 100
        throws += 3
        players[turn] = (players[turn] + total)
        while players[turn] > 10:
            players[turn] -= 10
        pts[turn] += players[turn]
        turn = 1 if turn == 0 else 0
    print(f'{pts}, throws: {throws}, res: {pts[turn] * throws}')

    # pt2
    all_throws = defaultdict(lambda: 0)
    for f in range(1, 4):
        for s in range(1, 4):
            for t in range(1, 4):
                all_throws[f + s + t] += 1

    players = [int(p.split(': ')[1]) for p in inp.strip().split('\n')]
    states = {0: {players[0]: {0: 1}},
              1: {players[1]: {0: 1}}}
    wins = [0, 0]
    i = 0
    while any(len(v) > 0 for k, v in states.items()):
        current_turn = i % 2
        player_stats = states[current_turn]
        new_stats = {}
        for total, possibilities in all_throws.items():
            for cur_pos, scores in player_stats.items():
                for old_score, old_paths in scores.items():
                    new_pos = cur_pos + total
                    while new_pos > 10:
                        new_pos -= 10
                    new_score = old_score + new_pos
                    path_score = old_paths * possibilities
                    if new_score >= 21:
                        opponent = states[(current_turn + 1) % 2].values()
                        for op_scores in opponent:
                            for k, v in op_scores.items():
                                wins[current_turn] += v * path_score
                    else:
                        if new_pos not in new_stats:
                            new_stats[new_pos] = {new_score: path_score}
                        else:
                            if new_score in new_stats[new_pos]:
                                new_stats[new_pos][new_score] += path_score
                            else:
                                new_stats[new_pos][new_score] = path_score
        states[current_turn] = new_stats
        i += 1
    print(max(wins))


sample_input = r"""
Player 1 starting position: 4
Player 2 starting position: 8
"""

real_input = r"""
Player 1 starting position: 8
Player 2 starting position: 9
"""


if len(sample_input.strip()) > 0:
    print("sample:")
    start = timer()
    main(sample_input, False)
    end = timer()
    print(f'sample: {(end-start)*1000_000:.0f}μs ({(end-start)*1000:.0f}ms)')


print("real:")
start = timer()
main(real_input, True)
end = timer()
print(f'sample: {(end-start)*1000_000:.0f}μs ({(end-start)*1000:.0f}ms)')
