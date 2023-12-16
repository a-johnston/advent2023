def valid(x, y, w, h):
    return x >= 0 and y >= 0 and x < w and y < h

def get_energy_calculator(grid):
    w, h = len(grid[0]), len(grid)
    energies = {}

    def inner(start):
        if start in energies:
            return energies[start]
        seen = set()
        energized = set()
        edge = {start}
        while edge:
            item = edge.pop()
            x, y, (dx, dy) = item
            if item in seen or not valid(x, y, grid):
                continue
            seen.add(item)
            energized.add((x, y))
            c = grid[y][x]
            if c == '.' or (c == '-' and dx != 0) or (c == '|' and dy != 0):
                edge.add((x + dx, y + dy, (dx, dy)))
            elif c == '\\':
                edge.add((x + dy, y + dx, (dy, dx)))
            elif c == '/':
                edge.add((x - dy, y - dx, (-dy, -dx)))
            elif c == '-':
                edge.add((x - 1, y, (-1, 0)))
                edge.add((x + 1, y, (1, 0)))
            elif c == '|':
                edge.add((x, y - 1, (0, -1)))
                edge.add((x, y + 1, (0, 1)))
            else:
                print(f'unknown! ({x}, {y}) ({dx}, {dy}) {c}')
        return len(energized)
    return inner

def solve_p1(lines):
    return get_energy((0, 0, (1, 0)), lines)

def get_starts(max_x, max_y):
    for x in range(max_x):
        yield (x, 0, (0, 1))
        yield (x, max_y - 1, (0, -1))
    for y in range(max_y):
        yield (0, y, (1, 0))
        yield (max_x - 1, y, (-1, 0))

def solve_p2(lines):
    return max(get_energy(start, lines) for start in get_starts(len(lines[0]), len(lines)))
