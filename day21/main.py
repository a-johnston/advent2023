offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))

def parse(lines):
    size = len(lines[1])
    steps = int(lines[0])
    grid, overlay = [], []
    padding = '#' * (len(lines[1]) + 2)
    lines = [padding] + ['#' + line + '#' for line in lines[1:]] + [padding]
    for line in lines:
        grid.append(int(line.replace('S', '1').replace('.', '1').replace('#', '0'), 2))
    return steps, grid, size

def create_overlay(size, pos=None):
    if pos is None:
        pos = int(size / 2), int(size / 2)
    overlay = [0] * (size + 2)
    overlay[pos[1] + 1] = 1 << (size - pos[0])
    return overlay

def print_overlay(overlay):
    for x in overlay:
        print(bin(x)[2:].zfill(len(overlay)))

def do_step(grid, overlay):
    new_overlay = [0] * len(overlay)
    for i, val in enumerate(overlay):
        if val == 0:
            continue
        new_overlay[i] |= val << 1
        new_overlay[i] |= val >> 1
        new_overlay[i - 1] |= val
        new_overlay[i + 1] |= val
    return [a & b for a, b in zip(grid, new_overlay)]

def get_score(overlay):
    return sum(map(int.bit_count, overlay))

def score_after_n(grid, overlay, steps):
    for _ in range(steps):
        overlay = do_step(grid, overlay)
    return get_score(overlay)

def solve_p1(lines):
    steps, grid, size = parse(lines)
    return score_after_n(grid, create_overlay(size), steps)

def get_even_odd_reach(grid, overlay):
    count = 0
    a, b, c = -2, -1, 0
    while a != c:
        overlay = do_step(grid, overlay)
        count += 1
        a, b, c = b, c, get_score(overlay)
    return (a, b) if count % 2 == 0 else (b, a)

def solve_p2(lines, steps=26501365):
    _, grid, size = parse(lines)
    r = int(size / 2)
    n = int((steps - r) / size)
    total = 0
    # Full inner tiles
    even, odd = get_even_odd_reach(grid, create_overlay(size))
    a, b = (even, odd) if n % 2 == 0 else (odd, even)
    total += (a * n ** 2) + (b * (n - 1) ** 2)
    # Edge tiles
    for pos in ((0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)):
        total += score_after_n(grid, create_overlay(size, pos), r - 1) * n
        total += score_after_n(grid, create_overlay(size, pos), size + r - 1) * (n - 1)
    # Cardinal tiles
    for pos in ((r, 0), (r, size - 1), (0, r), (size - 1, r)):
        total += score_after_n(grid, create_overlay(size, pos), size - 1)
    return total

def solve_p3(lines):
    return solve_p2(lines, 1000000000)
