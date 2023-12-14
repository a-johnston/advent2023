from itertools import pairwise

def parse(lines):
    rocks = set()
    blocks = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'O':
                rocks.add((x, y))
            elif c == '#':
                blocks.add((x, y))
    return rocks, blocks, (len(lines[0]), len(lines))

def valid(pos, size, *args):
    if pos[0] >= 0 and pos[1] >= 0 and pos[0] < size[0] and pos[1] < size[1]:
        return all(pos not in arg for arg in args)
    return False

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def find_right(values, count):
    for i in range(len(values) - 2, -1, -1):
        if values[i] == values[-1]:
            yield i
            count -= 1
            if count == 0:
                break
    for _ in range(count):
        yield -1

def try_detect_cycle(loads, limit):
    # This is not at all robust for general cycles but works for this problem..
    starts = list(find_right(loads, 3))
    deltas = set(b - a for b, a in pairwise(starts))
    if starts[-1] != -1 and len(deltas) == 1:
        delta = deltas.pop()
        for b, a in pairwise(starts):
            if loads[a:b] != loads[b:b + delta]:
                break
        else:
            return loads[starts[0] + ((limit - starts[1] - 1) % delta)]
    return -1

def calc_load(rocks, size):
    return sum(size[1] - pos[1] for pos in rocks), hash(tuple(sorted(rocks)))

def roll(rocks, blocks, size, moves, limit):
    rocks = set(rocks)
    cycles = 0
    loads = []
    while cycles < limit:
        cycles += 1
        for towards in moves:
            for pos in sorted(rocks, key=lambda pos: -dot(pos, towards)):
                rocks.remove(pos)
                maybe_pos = add(pos, towards)
                while valid(maybe_pos, size, rocks, blocks):
                    pos = maybe_pos
                    maybe_pos = add(pos, towards)
                rocks.add(pos)
        loads.append(calc_load(rocks, size))
        score = try_detect_cycle(loads, limit)
        if score != -1:
            return score[0]
    return loads[-1][0]

def get_total_load(lines, moves, limit):
    rocks, blocks, size = parse(lines)
    return roll(rocks, blocks, size, moves, limit)

def solve_p1(lines):
    return get_total_load(lines, [(0, -1)], 100)

def solve_p2(lines):
    return get_total_load(lines, [(0, -1), (-1, 0), (0, 1), (1, 0)], 1000000000)
