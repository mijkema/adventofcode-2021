from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer

class Node:

    def __init__(self, input, depth, parent):
        self.depth = depth
        self.parent = parent
        if isinstance(input, list):
            self.left = Node(input[0], depth + 1, self)
            self.right = Node(input[1], depth + 1, self)
            self.val = None
        else:
            self.val = input
            self.left = None
            self.right = None

    def __repr__(self) -> str:
        return str(self.val) if self.val is not None else format(f'[{self.left},{self.right}]')

    def is_leaf(self):
        return self.left is not None and self.left.val is not None \
               and self.right is not None and self.right.val is not None


def find_leaf(root):
    if root.is_leaf() and root.depth >= 4:
        return root
    if root.left:
        r = find_leaf(root.left)
        if r:
            return r
    if root.right:
        r = find_leaf(root.right)
        if r:
            return r
    return None


def find_left(leaf):
    current = leaf
    p = current.parent
    while p and p.left == current:
        current = p
        p = current.parent
    if p is None:
        return None

    to_add = p.left
    while to_add and to_add.val is None:
        to_add = to_add.right
    return to_add


def find_right(leaf):
    current = leaf
    p = current.parent
    while p and p.right == current:
        current = p
        p = current.parent
    if p is None:
        return None

    to_add = p.right
    while to_add and to_add.val is None:
        to_add = to_add.left
    return to_add


def find_high_value(root):
    if root.val is not None and root.val > 9:
        return root
    if root.left:
        r = find_high_value(root.left)
        if r:
            return r
    if root.right:
        r = find_high_value(root.right)
        if r:
            return r
    return None


def reduce(root):
    done = False
    while not done:
        done = True
        # bfs until leaf
        leaf = find_leaf(root)

        # explode first
        if leaf:
            done = False
            left_leaf = find_left(leaf)
            right_leaf = find_right(leaf)
            if left_leaf:
                left_leaf.val += leaf.left.val
            if right_leaf:
                right_leaf.val += leaf.right.val
            p = leaf.parent
            if p.left == leaf:
                leaf.parent.left = Node(0, leaf.depth, leaf.parent)
            else:
                leaf.parent.right = Node(0, leaf.depth, leaf.parent)
            continue

        # split after
        v = find_high_value(root)
        if v:
            done = False
            left = int(v.val / 2)
            right = int(v.val / 2)
            if v.val % 2 != 0:
                right += 1
            p = v.parent
            if p.left == v:
                p.left = Node([left, right], v.depth, p)
            if p.right == v:
                p.right = Node([left, right], v.depth, p)
    return root


def get_magnitude(root):
    if root.val is not None:
        return root.val
    return (3 * get_magnitude(root.left)) + (2 * get_magnitude(root.right))


def main(inp, is_real):
    inp = inp.strip().split('\n')
    root = None
    for i in inp:
        if root is None:
            root = Node(eval(i), 0, None)
        else:
            root = Node([eval(str(root)), eval(i)], 0, None)
            root = reduce(root)
    print(get_magnitude(root))

    max = 0
    for x in range(len(inp)):
        for y in range(len(inp)):
           res = get_magnitude(reduce(Node([eval(inp[x]), eval(inp[y])], 0, None)))
           if res > max:
               max = res
    print(max)


sample_input = r"""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

real_input = r"""
[[8,[[8,6],[6,0]]],[8,[[1,8],1]]]
[[[8,[7,5]],[8,8]],[1,5]]
[[[4,[4,5]],[[0,8],7]],3]
[[[8,[5,9]],8],[[6,[1,5]],7]]
[[[5,[0,8]],[0,[4,6]]],[[7,[4,7]],[[8,8],4]]]
[[5,[[4,4],5]],[3,[7,6]]]
[[2,[[4,9],[1,4]]],[4,0]]
[3,[[[4,7],6],4]]
[[[[0,5],8],4],[0,3]]
[[[1,8],[4,[3,2]]],[4,[4,[7,5]]]]
[[0,7],2]
[[[6,4],[0,4]],[[[5,7],[8,6]],2]]
[[[1,9],6],[[0,7],[3,1]]]
[[[4,2],[[1,6],4]],3]
[[[[2,9],[6,2]],6],[[[0,0],[3,5]],[[2,0],1]]]
[5,[[[0,4],[5,8]],2]]
[[[7,6],4],[[[2,5],6],2]]
[[1,6],[9,[[6,2],5]]]
[[1,[[5,6],3]],[[[6,4],[9,9]],[[3,8],1]]]
[[[[8,0],8],[[1,2],7]],[[1,1],[[5,1],[3,8]]]]
[[[8,[2,9]],[[3,0],[1,9]]],[3,9]]
[[[[9,8],[4,9]],[9,7]],1]
[[1,6],[4,5]]
[[[9,1],3],5]
[[[5,[3,2]],9],[[1,[9,3]],[[1,5],1]]]
[[8,[5,[2,1]]],[[[6,6],7],[1,[3,9]]]]
[[[[4,5],2],5],[[2,4],[2,8]]]
[[[[2,2],7],6],[4,[[8,5],[2,6]]]]
[[[[0,8],[6,4]],[[0,4],[6,5]]],[[3,[2,4]],[[3,2],7]]]
[[[8,[3,7]],[[5,3],5]],[[[9,3],[3,4]],1]]
[[2,[1,0]],[[[8,8],[4,7]],[[8,2],0]]]
[7,[8,3]]
[[[6,1],[[9,6],[3,8]]],[[[5,5],[7,1]],[[6,0],4]]]
[[[4,[1,3]],[[1,1],0]],[7,[[8,8],9]]]
[1,[[3,0],7]]
[[[[3,0],5],[[3,7],2]],[[[5,0],2],[0,[4,9]]]]
[[[[4,1],[0,1]],3],[[[2,1],[3,3]],[6,[9,2]]]]
[[[1,7],[5,9]],[[1,[7,7]],[[3,9],0]]]
[[[3,[1,0]],[[1,1],4]],[[4,3],[4,[2,0]]]]
[[[[5,1],[6,2]],[[4,9],[2,0]]],[2,[7,2]]]
[[[3,[8,6]],8],[[[9,1],[0,9]],[8,7]]]
[8,[[9,7],[[6,9],9]]]
[1,[[4,7],[5,[9,4]]]]
[[4,[[4,8],[8,8]]],[[[4,2],0],[[4,4],6]]]
[[[[1,1],[7,2]],[9,[0,7]]],[3,3]]
[[[2,[1,2]],6],[[[0,4],0],[5,[5,7]]]]
[6,[3,[4,7]]]
[[[1,4],[[1,3],[4,2]]],[6,8]]
[8,[[[6,1],1],8]]
[2,[2,[5,0]]]
[[[[6,1],[1,1]],[[4,9],[3,8]]],[[6,[6,6]],[6,2]]]
[[2,4],[1,4]]
[[[[6,0],[7,7]],[[4,1],[4,8]]],[[[6,4],8],9]]
[[1,[[0,5],3]],7]
[[[[2,9],6],[[0,9],6]],[8,7]]
[[4,6],[[[5,3],6],0]]
[4,[[3,[5,2]],[5,6]]]
[[8,[[4,8],6]],[[[9,8],5],9]]
[[[[8,7],6],[1,[3,0]]],[[5,[5,3]],6]]
[[[[5,8],9],7],[[[7,9],[0,2]],[[6,4],0]]]
[6,[[1,8],[[5,6],7]]]
[[7,[[4,8],9]],8]
[[[9,[6,4]],[1,3]],[0,7]]
[[[[1,8],[5,3]],5],[[[5,8],8],[[3,0],5]]]
[[[3,[6,7]],[2,9]],[[[7,1],1],[2,[4,1]]]]
[[8,[[9,5],[4,0]]],[[[4,3],3],[[0,8],[3,1]]]]
[[3,9],[[[6,5],[1,4]],6]]
[[2,[2,[9,0]]],[4,[0,6]]]
[[5,[8,9]],[[[9,2],4],1]]
[[5,[[8,2],[6,0]]],[9,[8,8]]]
[[[[8,8],1],[[3,4],[8,1]]],4]
[[9,[[7,2],[9,8]]],[[2,[4,9]],[[2,9],5]]]
[[[3,[9,1]],2],[0,[3,[0,3]]]]
[[9,[2,[6,2]]],[9,[9,[0,0]]]]
[[[[2,6],[2,0]],5],[[[7,9],5],[[1,5],6]]]
[[1,[[6,3],1]],[[[4,1],[0,7]],2]]
[[[[0,9],2],[[8,5],9]],[[1,[1,7]],6]]
[[[0,[8,3]],3],[[[1,9],0],[[7,2],4]]]
[[[[2,2],5],[[1,6],5]],[[[4,8],2],[[3,2],[4,8]]]]
[[[8,[6,8]],6],[0,[[3,2],7]]]
[[7,[[2,0],9]],[[4,[2,4]],[[8,8],[4,5]]]]
[[4,[[5,2],6]],[[0,7],2]]
[[4,3],[[5,[2,1]],[8,[3,3]]]]
[[[[6,1],9],4],2]
[3,[[[8,0],[3,7]],[[2,9],[6,6]]]]
[6,[[3,3],[9,[3,6]]]]
[[[9,[9,4]],3],[[1,0],0]]
[[[[1,1],[4,5]],[8,1]],[8,[2,2]]]
[[6,[0,3]],0]
[[[[3,2],8],6],[[9,[0,6]],[5,6]]]
[[4,[[4,8],[2,5]]],[[8,8],[[9,9],3]]]
[[6,7],[[8,[9,1]],[[6,3],[3,5]]]]
[2,[[3,[0,7]],[[7,4],5]]]
[[[1,4],9],[1,[[1,4],[0,1]]]]
[[[8,[9,7]],7],[[8,4],[[5,2],[5,5]]]]
[[[[9,8],[0,0]],8],[[3,[7,4]],[[0,1],[3,9]]]]
[[[[2,3],[0,0]],0],[[0,1],[[4,9],0]]]
[[8,[[5,3],2]],[[[2,9],2],[2,0]]]
[[[[2,2],[6,1]],[2,[6,6]]],[5,0]]
[[7,3],[[1,5],[[8,7],[3,1]]]]
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
