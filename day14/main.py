from itertools import pairwise

def parse(lines):
    lines.insert(0, '#' * len(lines[0]))
    lines.append(lines[0])
    rocks = set()
    grid = []
    for y, line in enumerate(lines):
        line = '#' + line + '#'
        grid.append(list(line))
        for x, c in enumerate(line):
            if c == 'O':
                rocks.add((x, y))
    return rocks, grid

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
    return None

def calc_load(rocks, size):
    return sum(size - pos[1] - 1 for pos in rocks)

def roll(rocks, grid, moves, limit):
    cycles = 0
    loads = []
    while cycles < limit:
        cycles += 1
        key = 0
        for towards in moves:
            dx, dy = towards
            for pos in sorted(rocks, key=lambda pos: -pos[0] * dx - pos[1] * dy):
                x, y = pos
                mx = x + dx
                my = y + dy
                if grid[my][mx] == '.':
                    rocks.remove(pos)
                    grid[y][x] = '.'
                    while grid[my][mx] == '.':
                        mx += dx
                        my += dy
                    x = mx - dx
                    y = my - dy
                    rocks.add((x, y))
                    grid[y][x] = 'O'
                key += x * 123 + y
        loads.append((calc_load(rocks, len(grid)), key))
        score = try_detect_cycle(loads, limit)
        if score is not None:
            return score[0]
    return loads[-1][0]

def get_total_load(lines, moves, limit):
    rocks, grid = parse(lines)
    return roll(rocks, grid, moves, limit)

def solve_p1(lines):
    return get_total_load(lines, [(0, -1)], 100)

def solve_p2(lines):
    return get_total_load(lines, [(0, -1), (-1, 0), (0, 1), (1, 0)], 1000000000)
