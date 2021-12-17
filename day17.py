from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


def inside(point, x_range, y_range):
    return x_range[0] <= point[0] <= x_range[1] and y_range[0] <= point[1] <= y_range[1]


def main(inp, is_real):
    inp = inp.strip().split(': ')[1].split(', ')
    x_range = [int(n) for n in inp[0][2:].split('..')]
    y_range = [int(n) for n in inp[1][2:].split('..')]

    # determine highest y
    highest_y = 0

    all_options = 0
    for start_x in range(x_range[1] + 1):
        for start_y in range(-100, 100):
            current = (0, 0)
            points = [current]
            x_dir = start_x
            y_dir = start_y
            while current[1] >= y_range[0]:
                current = (current[0] + x_dir, current[1] + y_dir)
                x_dir = max(0, x_dir - 1)
                y_dir -= 1
                points.append(current)
                if inside(current, x_range, y_range):
                    all_options += 1
                    res = max([n[1] for n in points])
                    if res > highest_y:
                        highest_y = res
                    break

    print(f'highest y: {highest_y}, total options: {all_options}')


sample_input = r"""
target area: x=20..30, y=-10..-5
"""

real_input = r"""
target area: x=269..292, y=-68..-44
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
