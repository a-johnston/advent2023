from collections import defaultdict
from itertools import pairwise

DIRS = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
CONV = 'RDLU'

def parse(lines):
    data = []
    for line in lines:
        a, b, c = line.split()
        data.append((a, int(b), c.strip('()')))
    return data

def extract(commands):
    for direction, distance, color in commands:
        new_direction = CONV[int(color[-1])]
        new_distance = int(color[1:-1], 16)
        new_color = f'#{hex(distance)[2:]:>05}{CONV.index(direction)}'
        yield new_direction, new_distance, new_color

def legal(int_range):
    return int_range[1] > int_range[0]

def xor_range(range_a, range_b):
    a1, b1 = min(range_a, range_b)
    a2, b2 = max(range_a, range_b)
    if b1 < a2:
        yield (a1, b1)
        yield (a2, b2)
    elif b1 == a2:
        yield (a1, b2)
    elif b1 <= b2:
        yield (a1, a2)
        yield (b1, b2)
    else:
        yield (a1, a2)
        yield (b2, b1)

def or_range(range_a, range_b):
    a1, b1 = min(range_a, range_b)
    a2, b2 = max(range_a, range_b)
    if b1 < a2:
        yield (a1, b1)
        yield (a2, b2)
    else:
        yield (a1, max(b1, b2))

def op_ranges(op, ranges, new_range):
    new_ranges = [new_range]
    for r in ranges:
        if new_ranges:
            latest = new_ranges.pop()
            new_ranges.extend(filter(legal, op(latest, r)))
        else:
            new_ranges.append(r)
    return new_ranges

def xor_ranges(ranges, new_range):
    return op_ranges(xor_range, ranges, new_range)

def or_ranges(ranges, new_range):
    return op_ranges(or_range, ranges, new_range)

def get_width(ranges):
    return sum(b - a for a, b in ranges) + len(ranges)

def dig(commands):
    dirt = defaultdict(list)
    x, y = 0, 0
    for direction, distance, color in commands:
        sx = x
        dx, dy = DIRS[direction]
        x += dx * distance
        y += dy * distance
        if x != sx:
            dirt[y].append((min(sx, x), max(sx, x)))
    ranges = []
    total = 0
    width = 0
    yprev = min(dirt)
    for y, x_ranges in sorted(dirt.items()):
        total += width * (y - yprev)
        boundary = ranges
        for x_range in x_ranges:
            ranges = xor_ranges(ranges, x_range)
            boundary = or_ranges(boundary, x_range)

        width = get_width(ranges)
        total += get_width(boundary)
        yprev = y + 1
    return total

def solve_p1(lines):
    return dig(parse(lines))

def solve_p2(lines):
    return dig(extract(parse(lines)))
