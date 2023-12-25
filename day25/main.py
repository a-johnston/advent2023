from random import choice

def parse(lines):
    edges = []
    nodes = set()
    for line in lines:
        this, r = line.split(': ')
        nodes.add(this)
        for other in r.split():
            nodes.add(other)
            edges.append((this, other))
    return nodes, edges

def karger(nodes, edges):
    ntn = {node: {node} for node in nodes}
    nodesets = list(ntn.values())
    while len(nodesets) > 2:
        a, b = choice(edges)
        if ntn[a] == ntn[b]:
            continue
        ntn[a].update(ntn[b])
        for c in ntn[b]:
            if ntn[c] in nodesets:
                nodesets.remove(ntn[c])
            ntn[c] = ntn[a]
    cut = 0
    for a, b in edges:
        if ntn[a] is not ntn[b]:
            cut += 1
    return cut, nodesets

def solve_p1(lines):
    nodes, edges = parse(lines)
    while True:
        cut, groups = karger(nodes, edges)
        if cut == 3:
            return len(groups[0]) * len(groups[1])
