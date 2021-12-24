import copy
import random
from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


class World:
    costs = {'A': [1, 0, 2], 'B': [10, 1, 4], 'C': [100, 2, 6], 'D': [1000, 3, 8]}
    mapping = {2: 0, 4: 1, 6: 2, 8: 3}

    def __init__(self, inp_str=None, hallway=None, rooms=None, inp_world=None, cost=0):
        if inp_str:
            inp = inp_str.split('\n')
            self.room_depth = len(inp) - 3
            self.hallway = inp[1].replace('#', '')
            self.hall_len = len(self.hallway)
            self.rooms = ['', '', '', '']
            for j in range(self.room_depth):
                for i, c in enumerate(list(inp[j+2].replace('#', '').replace(' ', ''))):
                    self.rooms[i] += c
            self.worlds_before = []
        if hallway:
            self.hallway = hallway
            self.hall_len = inp_world.hall_len
            self.room_depth = inp_world.room_depth
            self.rooms = rooms
            self.worlds_before = [w for w in inp_world.worlds_before]
        self.hash = self.hallway + ''.join(self.rooms)
        self.cost = cost
        self.worlds_before.append(self)

    def __repr__(self) -> str:
        res = self.hallway + '\n'
        for j in range(self.room_depth):
            res += f' #{self.rooms[0][j]}#{self.rooms[1][j]}#{self.rooms[2][j]}#{self.rooms[3][j]}#\n'
        res += 'cost: ' + str(self.cost) + '\n'
        return res

    def can_move(self, pos, v):
        if v not in self.costs.keys():
            return False
        if pos[0] == self.costs[v][2] and all([a == v or a == '.' for a in self.rooms[self.costs[v][1]]]):
            return False
        if pos[1] > 1:
            if self.rooms[World.mapping[pos[0]]][pos[1] - 2] != '.':
                return False
        return True

    def find_moves(self, pos, v):
        # v is in a position that it could move
        res = []
        moves = pos[1]
        # try to go left
        cur_pos = [pos[0], 0]
        cur_dist = 0
        while cur_pos[0] - 1 >= 0 and self.hallway[cur_pos[0] - 1] == '.':
            cur_pos = [cur_pos[0] - 1, cur_pos[1]]
            cur_dist += 1
            if cur_pos[0] not in World.mapping.keys():
                res.append(self.make_world(pos, cur_pos, (moves + cur_dist) * World.costs[v][0], v))

            # if it is above its correct room it can go in it
            if cur_pos[0] == World.costs[v][2]:
                room = self.rooms[World.mapping[cur_pos[0]]]
                if all([r == v or r == '.' for r in room]):
                    depth = len([t for t in room if t == '.'])
                    res.append(self.make_world(pos, [cur_pos[0], depth], (moves + cur_dist + depth) * World.costs[v][0], v))

        # try to go right
        cur_pos = [pos[0], 0]
        cur_dist = 0
        while cur_pos[0] + 1 < len(self.hallway) and self.hallway[cur_pos[0] + 1] == '.':
            cur_pos = [cur_pos[0] + 1, cur_pos[1]]
            cur_dist += 1
            if cur_pos[0] not in World.mapping.keys():
                res.append(self.make_world(pos, cur_pos, (moves + cur_dist) * World.costs[v][0], v))

            # if it is above its correct room it can go in it
            if cur_pos[0] == World.costs[v][2]:
                room = self.rooms[World.mapping[cur_pos[0]]]
                if all([r == v or r == '.' for r in room]):
                    depth = len([t for t in room if t == '.'])
                    res.append(self.make_world(pos, [cur_pos[0], depth], (moves + cur_dist + depth) * World.costs[v][0], v))
        return res

    def find_moves_in_hallway(self, pos, v):
        cur_pos = [pos[0], pos[1]]
        d = 1 if pos[0] < World.costs[v][2] else -1
        cur_dist = 0
        while cur_pos[0] + d != World.costs[v][2]:
            if self.hallway[cur_pos[0] + d] != '.':
                return []
            cur_pos = [cur_pos[0] + d, cur_pos[1]]
            cur_dist += 1
        cur_pos[0] += d
        cur_dist += 1
        if World.costs[v][2] == cur_pos[0]:
            room = self.rooms[World.mapping[cur_pos[0]]]
            if all([r == v or r == '.' for r in room]):
                depth = len([t for t in room if t == '.'])
                return [self.make_world(pos, [cur_pos[0], depth], (cur_dist + depth) * World.costs[v][0], v)]
        return []

    def moves(self):
        res = []
        for i, v in enumerate(self.hallway):
            if self.can_move([i, 0], v):
                res.extend(self.find_moves_in_hallway([i, 0], v))
        for x, r in enumerate(self.rooms):
            for y, v in enumerate(r):
                coords = [2 + (x * 2), y + 1]
                if self.can_move(coords, v):
                    res.extend(self.find_moves(coords, v))
        return res

    def make_world(self, pos, new_pos, distance, v):
        new_hallway = self.hallway
        new_rooms = [r for r in self.rooms]
        if new_pos[1] == 0:
            new_hallway = new_hallway[:new_pos[0]] + v + new_hallway[new_pos[0] + 1:]
        else:
            r = new_rooms[World.mapping[new_pos[0]]]
            p = new_pos[1] - 1
            if p == 0:
                new_rooms[World.mapping[new_pos[0]]] = v + r[1:]
            else:
                new_rooms[World.mapping[new_pos[0]]] = r[:p] + v + r[p+1:]

        if pos[1] == 0:
            new_hallway = new_hallway[:pos[0]] + '.' + new_hallway[pos[0] + 1:]
        else:
            r = new_rooms[World.mapping[pos[0]]]
            p = pos[1] - 1
            if p == 0:
                new_rooms[World.mapping[pos[0]]] = '.' + r[1:]
            else:
                new_rooms[World.mapping[pos[0]]] = r[:p] + '.' + r[p+1:]
        return World(inp_world=self, hallway=new_hallway, rooms=new_rooms, cost=self.cost+distance)


def main(inp, is_real):
    solution = '...........AAAABBBBCCCCDDDD'
    inp = inp.strip()
    world = World(inp)
    visited = set()
    unvisited = {0: [world]}
    min_dist = 0
    m = {world.hash: world}
    states = {world.hash: 0}
    min_cost = sys.maxsize
    while unvisited:
        current = unvisited[min_dist].pop()
        for n in current.moves():
            s = n.hash
            if s == solution and n.cost < min_cost:
                print(f'found a solution in {n.cost}')
                min_cost = n.cost
            m[s] = n
            if s not in visited and (s not in states or n.cost < states[s]) and n.cost <= min_cost:
                states[s] = n.cost
                if s not in visited:
                    if n.cost not in unvisited:
                        unvisited[n.cost] = [n]
                    else:
                        unvisited[n.cost].append(n)
        visited.add(current.hash)
        if len(unvisited[min_dist]) == 0:
            del unvisited[min_dist]
            min_dist = sys.maxsize if len(unvisited.keys()) == 0 else min(unvisited.keys())
    print(states[solution])


sample_input = r"""
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
"""

real_input = r"""
#############
#...........#
###B#B#D#A###
  #D#C#B#A#
  #D#B#A#C#
  #D#C#A#C#
  #########
"""

if len(sample_input.strip()) > 0:
    print("sample:")
    start = timer()
    main(sample_input, False)
    end = timer()
    print(f'sample: {(end - start) * 1000_000:.0f}μs ({(end - start) * 1000:.0f}ms)')

print("real:")
start = timer()
main(real_input, True)
end = timer()
print(f'sample: {(end - start) * 1000_000:.0f}μs ({(end - start) * 1000:.0f}ms)')
