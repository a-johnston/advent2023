from collections import defaultdict

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

connectors = {
    '|' : (N, S),
    '-' : (E, W),
    'L' : (N, E),
    'J' : (N, W),
    '7' : (W, S),
    'F' : (E, S),
}

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def get_deltas(pos, edges):
    h, v, ah, av = 0, 0, 0, 0
    for edge in edges:
        dh, dv = edge[0] - pos[0], edge[1] - pos[1]
        h += dh
        v += dv
        ah += abs(dh)
        av += abs(dv)
    return h, v, ah, av

def parse(lines):
    nodes = {}
    edges = defaultdict(set)
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '.':
                continue
            if c == 'S':
                start = (x, y)
            nodes[(x, y)] = c
    for pos, kind in nodes.items():
        for con in connectors.get(kind, ()):
            other = add(pos, con)
            if other in nodes:
                edges[pos].add(other)
                if other == start:
                    edges[other].add(pos)
    loop = {}
    search = {start}
    while search:
        node = search.pop()
        loop[node] = (nodes[node], edges[node])
        for other in edges[node]:
            if other not in loop:
                search.add(other)
    return loop

def solve_p1(lines):
    return int(len(parse(lines)) / 2)

def solve_p2(lines):
    loop = parse(lines)
    min_x, min_y = min(x for x, y in loop), min(y for x, y in loop)
    max_x, max_y = max(x for x, y in loop), max(y for x, y in loop)
    total = 0
    for y in range(min_y - 1, max_y + 2):
        vert = 0
        inside = False
        for x in range(min_x - 1, max_x + 2):
            pos = (x, y)
            node = loop.get(pos)
            if node is not None:
                h, v, ah, av = get_deltas(pos, node[1])
                if av == 2 or (v != 0 and vert != 0 and v != vert):
                    inside = not inside
                    vert = 0
                elif v != 0:
                    vert = v if vert == 0 else 0
            elif inside:
                vert = 0
                total += 1
    return total
