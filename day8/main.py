import itertools
import math

def parse(lines):
    moves = lines[0].replace('L', '0').replace('R', '1')
    moves = map(int, itertools.cycle(moves))
    nodes = {}
    for line in lines[2:]:
        l, r = line.split(' = ')
        nodes[l] = r[1:-1].split(', ')
    return moves, nodes

def solve_p1(lines):
    moves, nodes = parse(lines)
    node = 'AAA'
    steps = 0
    while node != 'ZZZ':
        steps += 1
        node = nodes[node][next(moves)]
    return steps

def solve_p2(lines):
    moves, nodes = parse(lines)
    node = [n for n in nodes if n[-1] == 'A']
    cycle = [None] * len(node)
    steps = 0
    while any(c is None for c in cycle):
        steps += 1
        move = next(moves)
        for i in range(len(node)):
            node[i] = nodes[node[i]][move]
            # NB: This used to also test for cycle offsets but those were all
            #  zero so I removed that code
            if node[i][-1] == 'Z' and cycle[i] is None:
                cycle[i] = steps
    return math.lcm(*cycle)
