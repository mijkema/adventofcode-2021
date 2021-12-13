from collections import defaultdict, Counter
from curses.ascii import isupper
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


def find_paths(graph, node, visited, double_cave):
    res = []
    for e in graph[node]:
        path = visited.copy()
        path.append(e)
        twice = double_cave
        if e == 'end':
            res.append(path)
        else:
            # Small caves are only allowed < 2 times
            if e.islower() and e in visited:
                if not double_cave:
                    twice = True
                else:
                    continue
            for p in find_paths(graph, e, path, twice):
                res.append(p)
    return res


def make_graph(inp):
    res = {}
    for edge in inp:
        if edge[1] not in res:
            res[edge[1]] = []
        if edge[0] not in res:
            res[edge[0]] = []
        if edge[1] != 'start':
            res[edge[0]].append(edge[1])
        if edge[0] != 'start':
            res[edge[1]].append(edge[0])
    return res


def main(inp, is_real):
    # if is_real: return
    inp = [tuple(n.split('-')) for n in inp.strip().split('\n')]
    graph = make_graph(inp)

    # breadth first search
    print(len(find_paths(graph, 'start', ['start'], False)))


sample_input = r"""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

real_input = r"""
by-TW
start-TW
fw-end
QZ-end
JH-by
ka-start
ka-by
end-JH
QZ-cv
vg-TI
by-fw
QZ-by
JH-ka
JH-vg
vg-fw
TW-cv
QZ-vg
ka-TW
ka-QZ
JH-fw
vg-hu
cv-start
by-cv
ka-cv
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
