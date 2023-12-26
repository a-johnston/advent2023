from random import choice
from collections import defaultdict

def parse(lines):
    graph = defaultdict(set)
    for line in lines:
        this, r = line.split(': ')
        for other in r.split():
            graph[this].add(other)
            graph[other].add(this)
    return graph

def solve(lines):
    graph = parse(lines)
    partition = set(graph)

    def count_out_edges(node):
        return len(graph[node] - partition)

    while sum(map(count_out_edges, partition)) != 3:
        partition.remove(max(partition, key=count_out_edges))

    return len(partition) * len(set(graph) - partition)
