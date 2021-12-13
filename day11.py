from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


def main(inp, is_real):
    if not is_real:
        return
    inp = [list(map(int, list(n))) for n in inp.strip().split('\n')]
    grid = defaultdict(lambda: 0)
    for x, row in enumerate(inp):
        for y, val in enumerate(row):
            grid[(x, y)] = val

    flashes = 0
    for step in range(10000):
        # increase by 1
        for k, v in grid.items():
            grid[k] += 1
        done = set()
        while True:
            # find > 9
            flash = None
            for x in range(len(inp)):
                for y in range(len(inp[0])):
                    if grid[(x, y)] > 9 and (x, y) not in done:
                        flash = (x, y)
            if flash is None:
                break
            for x in range(flash[0] - 1, flash[0] + 2):
                for y in range(flash[1] - 1, flash[1] + 2):
                    if (x, y) not in done:
                        grid[(x, y)] += 1
            done.add(flash)
            grid[flash] = 0
            flashes += 1
        if len(done) == len(inp) * len(inp[0]):
            print(f'at step {step}')
            exit(1)
    print(flashes)


sample_input = r"""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

real_input = r"""
7222221271
6463754232
3373484684
4674461265
1187834788
1175316351
8211411846
4657828333
5286325337
5771324832
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
