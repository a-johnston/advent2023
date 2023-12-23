E, W, N, S = (1, 0), (-1, 0), (0, -1), (0, 1)
DIRS = (E, W, N, S)
SLOPES = {'>': E, '<': W, 'v': S, '^': N}

class Node:
    def __init__(self, x, y, is_end=False):
        self.x = x
        self.y = y
        self.edges = {}
        self.is_end = is_end

def get_options(grid, x, y, directed):
    ret = set()
    if grid[y][x] == '#':
        return ret
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        c = grid[ny][nx]
        if c != '#' and (not directed or c not in SLOPES or SLOPES[c] == (dx, dy)):
            ret.add((nx, ny))
    return ret

def walk_passage(grid, x, y, nodes, ignore, directed):
    seen = {ignore}
    options = get_options(grid, x, y, directed) - seen
    seen.add((x, y))
    while (x, y) not in nodes and len(options) == 1:
        seen.add((x, y))
        x, y = options.pop()
        options = get_options(grid, x, y, directed) - seen
    return len(seen) - 1, x, y

def build_connections(grid, node, nodes, directed=False):
    x, y = node.x, node.y
    for nx, ny in get_options(grid, x, y, directed):
        l, ex, ey = walk_passage(grid, nx, ny, nodes, (x, y), directed)
        other = nodes.get((ex, ey))
        if other is not None:
            node.edges[other] = l

def parse(lines, use_directed):
    start = lines[0].index('.'), 1
    end = lines[-1].index('.'), len(lines)
    pad = ['#'] * len(lines[0])
    grid = [pad] + list(map(list, lines)) + [pad]
    nodes = {start: Node(*start), end: Node(*end, is_end=True)}
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            if len(get_options(grid, x, y, False)) > 2:
                nodes[(x, y)] = Node(x, y)
    for node in nodes.values():
        build_connections(grid, node, nodes, directed=use_directed)
    return nodes[start]

def get_longest(node, ignore=frozenset()):
    dist = 0
    ignore |= {node}
    for other, edge_dist in node.edges.items():
        if other in ignore:
            continue
        sublength = get_longest(other, ignore)
        if sublength == -1:
            continue
        if sublength + edge_dist > dist:
            dist = sublength + edge_dist
    return dist + 1 if dist > 0 or node.is_end else -1

def solve_p1(lines):
    return get_longest(parse(lines, True)) - 1

def solve_p2(lines):
    return get_longest(parse(lines, False)) - 1
