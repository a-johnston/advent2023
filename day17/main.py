from collections import namedtuple

Entry = namedtuple('Entry', ['position', 'facing', 'remaining', 'score'])

DIRS = ((-1, 0), (0, -1), (1, 0), (0, 1))

def parse(lines):
    return [list(map(int, line)) for line in lines]

def maybe_set_best(bests, entry):
    if entry.facing is None:
        return True
    any_set = False
    d = bests[entry.position[1]][entry.position[0]][entry.facing]
    for i in range(entry.remaining + 1):
        if entry.score < d[i]:
            d[i] = entry.score
            any_set = True
    return any_set

def path_sum(grid, min_move, max_move):
    r = max_move - min_move
    w, h = len(grid[0]), len(grid)
    start = (0, 0)
    end = (w - 1, h - 1)
    edge = {Entry(start, None, r, 0)}
    bests = [[[[1 << 32] * r for d in range(4)] for x in range(w)] for y in range(h)]

    while edge:
        entry = edge.pop()
        if entry.facing is None:
            dirs = (2, 3)
        else:
            dirs = ((entry.facing - 1) % 4, (entry.facing + 1) % 4)
        for d in dirs:
            dx, dy = DIRS[d]
            nx, ny = entry.position
            new_score = entry.score
            for i in range(-min_move, r):
                nx += dx
                ny += dy
                if nx < 0 or ny < 0 or nx >= w or ny >= h:
                    break
                new_score += grid[ny][nx]
                if i >= 0:
                    new_entry = Entry((nx, ny), d, r - i - 1, new_score)
                    if maybe_set_best(bests, new_entry):
                        edge.add(new_entry)
    return min(map(min, bests[end[1]][end[0]]))

def solve_p1(lines):
    return path_sum(parse(lines), 0, 3)

def solve_p2(lines):
    return path_sum(parse(lines), 3, 10)
