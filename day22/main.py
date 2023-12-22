from dataclasses import dataclass

X, Y, Z = 0, 1, 2

@dataclass
class Brick:
    idx: int
    A: list
    B: list
    supporting: set
    supported_by: set

    def __hash__(self):
        return hash(self.idx)

def parse(lines):
    bricks = []
    for line in lines:
        l, r = line.split('~')
        l = list(map(int, l.split(',')))
        r = list(map(int, r.split(',')))
        brick = Brick(len(bricks), l, r, set(), set())
        bricks.append(brick)
    return bricks

def get_low(brick, d=Z):
    return min(brick.A[d], brick.B[d])

def get_high(brick, d=Z):
    return max(brick.A[d], brick.B[d])

def delta(brick, d):
    x = brick.B[d] - brick.A[d]
    return 0 if x == 0 else int(x / abs(x))

def get_positions(brick):
    dx, dy, dz = delta(brick, X), delta(brick, Y), delta(brick, Z)
    pos = list(brick.A)
    while pos != brick.B:
        yield pos
        pos[X] += dx
        pos[Y] += dy
        pos[Z] += dz
    yield brick.B

def drop(bricks):
    min_x = min(get_low(brick, X) for brick in bricks)
    min_y = min(get_low(brick, Y) for brick in bricks)
    max_x = max(get_high(brick, X) for brick in bricks)
    max_y = max(get_high(brick, Y) for brick in bricks)
    max_z = max(get_high(brick, Z) for brick in bricks)
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    grid = [[(0, None)] * w for _ in range(h)]
    for brick in sorted(bricks, key=get_low):
        fall = max_z
        for x, y, z in get_positions(brick):
            x -= min_x
            y -= min_y
            fall = max(0, min(fall, z - grid[y][x][0] - 1))
            if fall == 0:
                break
        brick.A[Z] -= fall
        brick.B[Z] -= fall
        for x, y, z in get_positions(brick):
            x -= min_x
            y -= min_y
            top, other = grid[y][x]
            if z <= top:
                print('WARNING', brick, z)
            if top == z - 1 and other is not None and other != brick and brick not in other.supporting:
                other.supporting.add(brick)
                brick.supported_by.add(other)
            if top < z:
                grid[y][x] = (z, brick)
    return bricks

def can_safely_disintegrate(brick):
    return all(len(other.supported_by) != 1 for other in brick.supporting)

def is_stable(brick, ignore):
    if len(brick.supported_by) == 0:
        return True
    return len(brick.supported_by - ignore) > 0

def solve_p1(lines):
    return sum(map(can_safely_disintegrate, drop(parse(lines))))

def chainreaction(brick):
    drops = set()
    ignore = {brick}
    edge = list(brick.supporting)
    while edge:
        head = edge.pop(0)
        if head in drops:
            continue
        if not is_stable(head, ignore):
            drops.add(head)
            ignore.add(head)
            edge.extend(head.supporting)
    return len(drops)

def solve_p2(lines):
    return sum(map(chainreaction, drop(parse(lines))))
