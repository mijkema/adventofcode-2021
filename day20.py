from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


def print_grid(grid):
    max_x = max([p[0] for p in grid])
    min_x = min([p[0] for p in grid])
    max_y = max([p[1] for p in grid])
    min_y = min([p[1] for p in grid])
    res = ''
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if grid[(x, y)]:
                res += '#'
            else:
                res += '.'
        res += '\n'
    print(res)


def enhance(grid, algo, default_value):
    max_x = max([p[0] for p in grid])
    min_x = min([p[0] for p in grid])
    max_y = max([p[1] for p in grid])
    min_y = min([p[1] for p in grid])

    # all input elements flip on each step
    new_default_value = not default_value
    if algo[0] == '#' and algo[-1] == '.':
        new_grid = defaultdict(lambda: new_default_value)
    else:
        new_grid = defaultdict(lambda: False)

    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            neighbours = [grid[(x - 1, y - 1)], grid[(x - 1, y)], grid[(x - 1, y + 1)],
                          grid[(x, y - 1)], grid[(x, y)], grid[(x, y + 1)],
                          grid[(x + 1, y - 1)], grid[(x + 1, y)], grid[(x + 1, y + 1)]]
            index = int(''.join(['1' if n else '0' for n in neighbours]), 2)
            new_grid[(x, y)] = algo[index] == '#'
    return new_default_value, new_grid


def main(inp, is_real):
    algo, image = inp.strip().split('\n\n')

    image = image.split('\n')
    default_value = False
    grid = defaultdict(lambda: default_value)
    for x in range(len(image)):
        for y in range(len(image[0])):
            grid[(x, y)] = image[x][y] == '#'

    for i in range(50):
        default_value, new_grid = enhance(grid, algo, default_value)
        grid = new_grid
    print(len([k for k, v in grid.items() if v]))


sample_input = r"""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""

real_input = r"""
##..##...#..#.#...#.....##....#.#..#.#.####...#####..#.######...#......#.##.#..######.########....#.#..##.####.##...##..#.########.#.##..........##.######.#......#..#...##..#..#.###.#.#..#..#...##.###.....#.#.###..##.####....##.#....#.#.###..###.....####..###..##.#.#..##....#.#....#####.##.....#.#.#..###..#.....####..##.#..#.###....#...##..###.#.###.##.####..#.##......##.##.#.##..##...##..######..####.#.##..###..###.###.##.##..###..#.......##.#######.#..##..##.###.#.#.#.####...####..#.#.#.......##.##.#.....

.#####..###.#.##.#..#.#.###..#......##.####.####.....##..#..#..#.#.##..##..##..#...##..#####....#.#.
..###..##..##.#.##.###..#.##..##.########..#...####.#..#.#.#...##.##.##.#....####...#......###.#.#..
###.###.###.#..#.#.#.##.#..#.######.##.#..##...#.#...##......#.###...###.#.#.#..##...######.###..#..
.######..##.#.##.####.....#..###.##..###....##..#.#.....#.##.....##.####.#...##..###...##...#.##.#.#
##...#.#.##.#.###...#.##.#..##.#.##.##.#####...#.##..#..###.#.##...##...#.###.###.#.#.##.##..#......
..##....#.##.#....#.####.#.#...####..##...#..#.##.##.#.###.#..##.#..##......#####.#.###..#.##..##..#
..##.....#..#.#####.....#..####...###.#..#.##.#....#.##.#...####.##.....##........#...###.#.#.##.#.#
##..##.........##.#..##..#.####.#.........#.##.#..####..####.....#....#.#..##.###...#..#.#...#.#..##
....###.###.#....##.#...#..####..##.###.###.#.####.##.##.#####..####.####.#...#.#.#.....#.##.##.###.
#...#.#.###...#...#.#..##..#.##.#.##.##...#.#.#..#.##..#.#.....####...##.#####....#.#..#...#...##.#.
#.#...###....##..##...###..#..#####.#.###...##......##..###.##.#.#...#...#.#...###..#.####..#.......
.###....##.##...###.###.#.#.#.##..#..#..###..#..#.#..#.#....##....#.#.#.#....#.#.#..#.#.#..##..#....
###..#..##.###.#.####..####........#.#.##..##..#...#...#...##.##.#.....#.#..#..#..#.#...##...###.###
..##.#......#...###...###########.###..#.#..###....###..##.###..#....#######.#..###.##..###......###
..###..#.#.#.#.....####.#.#..#..#.####..#..#.#.##.##########.##.#.#.#....########.##...#..#..#.#..##
###....###.#.#....###.##...#..##.#..##...####....####.####...##..##.....#####.#......###.##..#..#...
#.###.#.#..#...#..#..#...#...#......#..###.####...##.#.###.....###.###..#...#...####.##..#.###.#.#..
##.###.##..##..#..#...####......##.#.#.#.###.#....##..###.#.##.#....#####..##..........#.##.#..#.#.#
.#.#.#.#####..##...#####..#####..###.#######....#..#.####..#.#..##....##.#..#.....#..###.##.#...#.#.
.#...#..#.....##....#.#####.##...###..#####..#.#####.#.#..####...#..###...#.###..###....#..#.##.....
#..##.##...###.##.#.#....##.....#.#.####...##.#.#..###....##.#..#..#.####.#.#.##.##.#.####.##.###.#.
.#..#.###...#..###.....####..##.##.....##.....#......#######...#.###..#.##.##....##.##.####..#######
#..#.#####.#.#.#..#.#.##..##.###....#####.##.##..#####.#..###..#...#.##........####...##..###.#...##
#.##.#..#...########.....##.####.#...##.#.##...#..##.#.#..##.....###..##...#######....####..##.#....
####.....####.##.##.##.######...#.####.#.#.#.#..##.##.#..####.#.#..#.##...#.#...##########..#.##..##
.##.#######.###.####..#....##...###..#.#.#..##....#......#.#...#.#..###..###...##.#######.#.####..##
..#.#......#...#######.#..#...######.#.#.#.#...##.#....######.#..#####.##.......#.#####....#####...#
####.####.##..#..#..###..###....#...###..#..#..#.##.##..##.##..###.####.####.##..##...###..##..#.###
.##.#......###.####..###..#....#..##.#.#.#.##.#...#.##...##.....#.######..######.##.#...####..###...
##.####.#.#..##..#.########.....#.##..#..#....#.#.#..#..#.#...##..#.#...##...#####.#...####.#######.
##.#..#.###.....#.##....#.#.#...#####.#.#######..##.#..#####.####..#.#.##.#..#...##.##.######.##..##
##..#.##..###...###..###....###.#....#.##...#.#.###......####.###..#######.#.#........##...#.#.##..#
#..##.#..#..####....#.###...#.#...##.#..#.#.####.#..##.###.##.##..#.##..#.##.##.#..#.....##....#..#.
#######.#.#.###.#####.....#.#..###..####.#...#...###..####.#..#.#.#.#.#...##...#.####.#.#.....#.####
##.###...####..##.#..#.#.##.#....#.###.###.####..####..####....###.###.##..###.#.##..##.#..#######.#
...###...#....######....###..#..#..##..###...###..###.####.####....##.#..#.#.#.#..#####.##.#..##..#.
#.....########.####.#....#.#####.#.....###.#.##..##...####.#.#.#.##..##.##.#.##.#####..#..#.##.##.#.
#..#.#.#......#.#.####.#.###.#.#.##..##.##.#...#..#.##..#.##.#..##.#...####.#.####.##.#......##.#.#.
####.#..#.##.######....##.....#.######.....###...##.##.....##.#...##..........#.#.##.##..#.##..#####
...###..##..#.#..####.#...#..#..##.#..##.#..####...#..#..##.#...#.##...##...###..#.####.......#..##.
.#.###.....#.####..#..#.##....###.##..##.#####.#...###.##.##..##.####.#..###.#####.##....#.##..###..
.#..##....##..#.##.##..##.....#..##.#.#....#..##.#..#.###..#.......###.##.###....####...##.#####..##
.#.##.#.#....####..####.#......#.....#####.#.####...#.##.#...###.#.#..##.#.##.#.##..##.#######...#..
##..###.#..#.#..#...###.....#.#....##.##.#.##.##.#..######...#..#..#.......###.#.####...#.######...#
#...###..#......#..#...#....###.....##.##.##.##....#####.##....##.##.#....##..#...##..#.##..#.#.#..#
.....#.#.###.#.####..#....####.#####......##.##..####.#.#.#....#..#....######.#.###...###..###..#...
.#.#.#.#....#.#.....##..#...##.##.#..###.#.#.#.###......#.############.#............#..#..##.......#
#.##.#..####.##.##..##..#.####.#...##.##..#####.###..##..#.######.#.###....#.##..##..#....#..####...
#..###...###..#.##....#......##...###...##..#..#..#.#.#.#.##....#......##..##.#.#.####..##..#..#.##.
#.#.....##...#...#####...#.#####....#..###..#..#..####.##.#..##..#.###..#...#.#.#.##..##.#.....##.#.
..#.###..##.###..###.....#.###.#######.#.....#.#####.#...####.....#...#######..#.#.#.#..##.##.#.##..
####...#.#..#.##..#.##....#..####..#..####...##.#....###..#..#..#.#.###...#..#####...#.##.##.##..#..
.#.#..##.######..##.#.##...##...#.........#..#.###....#..#....####.##....#####..#....##.####..#.####
.#..##....#..##....#.###.######.#..#..#.###.####.#.#.#..####...###.##.##..#..#...#..#.###.##.###.###
......###.#..#..#..#.#.#.#...#.#..#...#....#.##..#.##.#.....##....####.#..##..##....#..#.#.##.#..##.
#..##.##..#######.#...##....#..###.#.##.###.##.###..#.###.#...#.#...##.#.###....###.#.##.#.#....#.##
#...####..######...####.#.##..###..#.#####.##...#.####.#.#....####.#..#.......###...##.#..#..##...##
##..#..##.#.###.#.#..#.#.###..#.......###..#.#.#.###........#...#.#..#.....##.####...#####.###....##
...#...#######.#..#########.#.#..#..###..#.#..#######.#.#....#.#.##.###.###.#######.####.....##.#.#.
..#...#####.#.##...##...#.#.##.#.###.#..###.#.#...##.#..#.#..###.#..#.#....#.###..###.#..##.....####
.#.###.#.#..#.####..#.###....##..#.#...##..#.###.#.#.##..#.#.#.....##.#...##.##..#.....#..##.#.###.#
#..#.###.##..#..###....#...#.#.###..#....####.##.##.#.#...#..#..####.##.##.##.###...####...####....#
.#.#...##.#.##.....#.#.##..#.#...#.#.#...##.....##.#...#####...##..##...#..##.##.##.#.##.##.....##.#
.######.###..#.#.######.###.#.#...#..#.#.#..#..##......####.##...#..#.#.#.###..####.##.######.######
.##.##...#......##.#....######.##.###.####...##...##.#.#.#.#.##...#######..#....##.#..#....###......
.#.##.###....#..#..#...###...#...#.#.....###.##.###.#........##.#.##.###..##.#####.##..##.##.#.#.#.#
..##..####.##.#..###.##.#..###.###.#####.####.#.##.####..#...#..#.###.#.#....#.##..##.#..##....##..#
.....#.#..##...#.#..##.#..#.#########..##.##.#...###..######...#.#.....#...###.##..##..#.#.......#.#
..#.#.#.#...###..####.###.##..#.##.###..#.#...##.....#.#..###.#..#.###..#.###..###.#.##...####.#....
#..#.###..#.#.##.#..##.###...##..............##.###.#.##...#.##..#...##........#.#.###.##....#.#.##.
##....####.##.#......###..#.....#.....#..####.....#..#.#.####...###...#...#.#...####..#..#..#..###..
.#....#..#####....#.#.#.#...#....##....##.#..###.#....#.#######.#.####.##...##..#....#......#.#.#.##
#.##....#####.#######...#.####.#..#..##..#.######..####..####..#..#...#.#.###.###....#..#....#.#####
###.#####...#.##.#.#####.#.#################.#..#..##.##...#.#...###..#.#.#.##.##..###.#..##.##..###
.#.##.##.###.#.##.#.###.##....#.....##..##...##.#########.##.##.#.###..##..#..#.#####..###.#...#..##
#.#....###..#.###..#...#..#.###.#.##..#..#.##...#...#..##..###..######....#.##.#..#.........##.#.##.
#.#.##.#.#####.#.#..#..###..#...###.###..##.##...##....#..##..##....#....#...##.#####..###..#..####.
#.#..##..##..##..##...####.#..#.####.##.#.##..#....###.#.####.####..#.###.###.#.#..#.#...#.#..#.....
#.#...####..#######.#.##..#.#......##.....######..#..##...##.#..#.#####.#..#..#....#.#..#####.#...##
.#.#.######.##....#..###.#...#.#....#.......#..#.#.#..#....##.#..###..##..#.#......####.#.#.##...##.
##..###..####...###.####...#.###....#.#######.##.####.#.....#.#.###.####.####...#.#.....#....##..###
..#.#.#.#.###...##.##..##..#.######..###..#...#......##.#.###....#.###...#.....#....####..###.##.#.#
.###..##..###.....##...#......####.##.#....###..#.##.#..#.##.##..#.....#.#.##..##.####..###.#...#..#
.#....####..##.#...###.#..#..###..##.#.#.....#...#.###..####..######.#.#...#...#.#...##.....###.....
.....#.#...#...#..#.###....##.##.#.#.#.#.##...##.#.#.....#.###.#.#.##.######.....#.###.###.#.##.###.
.####....#..###.#####.#.#..#.#.#..##.....##.#.#.#...#####..##.#.......###.###.#.##.#..##.#.###.#.#.#
##.#.#......#####..#.##.##..###..##..###.#..##..##.#.###.....#...####......#..###....#..##.#..#....#
#.#.#####...##.##.#...##.###..######.###.#.##.##..#..#...##..##.###...#.#..##.#########.#####.#.##.#
.#.##....#..#..#..#..##...#......#..#.#.##...##...#.###.##.......####...#.#..#.#...##.#..#.####..##.
.#.######.#.##...#####.###..#..##....##.#####.###..######.#...###.#.##..##....###..####.##.#.####.##
.#.#....#.##..##...#########...#..#.#.######.#.#.##.#....####.#...#.##..#..#.#.#..#.#.##..#.#...#.#.
.####...#...#..##.#.#.###.####...#.#...#####.....###.####.#.##..###..#.##.#...#.#####.####..##.##.#.
....#..#...#.###..##.##..#..####.#.#...#.#####..##...#####.#.#...###..#...#.#.###.#.#.##..###..###.#
#####.........##..###.#.###.#..........#.#.#..#.#..#.#.#######.#....##....#.###..#.#..##.#...##....#
.....###.##..#....#..#.#...#.##.#..#.#####.####.##.#.#.###........##..#.#..#.....###......##..##.#..
.###....#.#....#......##.##....##....#.#.##.######.#.##..##.###...#....#..#..#..###..##.#.#.##.#.#.#
##....#.##.#..#.###..##.##..#.#..###.##........##.#.#..#..####...####.#...#....#.#.##..#...#.####.#.
....###.##.#####.#....##.##.##.#..#.#..#.##.##.#.####.##..#.##.#...##..####..#..#.#.##.##...##.#....
..###........####.#....##.##..##..##.#....###..#.#.###......#.#####.###...##..##..#..#.#.###.#.#..#.
....#.###.##.....#..#.#.#.#####.###.#.##.#.##.......#.###.#.##..###........#.#.###.####.##.#....#.#.
"""


if len(sample_input.strip()) > 0:
    print("sample:")
    start = timer()
    main(sample_input, False)
    end = timer()
    print(f'sample: {(end-start)*1000_000:.0f}??s ({(end-start)*1000:.0f}ms)')


print("real:")
start = timer()
main(real_input, True)
end = timer()
print(f'sample: {(end-start)*1000_000:.0f}??s ({(end-start)*1000:.0f}ms)')
