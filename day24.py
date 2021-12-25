import random
from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *

import statistics
import numpy
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


def evaluate(ins, vals, inp=0):
    if ins[0] == 'inp':
        vals[ins[1]] = inp
        return vals

    second = ins[2]
    if second in vals:
        second = vals[second]
    if ins[0] == 'add':
        vals[ins[1]] += second
    if ins[0] == 'mul':
        vals[ins[1]] *= second
    if ins[0] == 'div':
        if second == 0:
            raise Exception('division by 0')
        vals[ins[1]] //= second
    if ins[0] == 'mod':
        if vals[ins[1]] < 0 or second <= 0:
            raise Exception('invalid mod operation')
        vals[ins[1]] %= second
    if ins[0] == 'eql':
        vals[ins[1]] = 1 if vals[ins[1]] == second else 0
    return vals


def get_value(to_try, instructions):
    indx = 0
    current = to_try[indx]
    vals = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for ins in instructions:
        vals = evaluate(ins, vals, inp=current)
        if ins[0] == 'inp':
            indx += 1
            if indx < len(to_try):
                current = to_try[indx]
    return vals


def main(inp, is_real):
    if not is_real: return
    inp = inp.strip().split('\n')
    instructions = []
    for i in inp:
        parts = i.split(' ')
        if len(parts) > 2:
            try:
                parts[2] = int(parts[2])
            except ValueError:
                parts[2] = parts[2]
        instructions.append(parts)


    print(get_value([9, 9, 2, 9, 9, 5, 3, 1, 8, 9, 9, 9, 7, 1], instructions))



sample_input = r"""
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""

real_input = r"""
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 0
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -3
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
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
