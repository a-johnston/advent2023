from random import random 
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

    def key(node):
        return count_out_edges(node) + random() * 0.5

    while sum(map(count_out_edges, partition)) != 3:
        if not partition:  # Reset process if we happen to get unlucky
            partition = set(graph)
        partition.remove(max(partition, key=key))

    return len(partition) * len(set(graph) - partition)
