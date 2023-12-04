from collections import defaultdict

def parse(line):
    idx, line = line[len('Card '):].split(': ')
    l, r = map(lambda x: set(map(int, x.split())), line.split(' | '))
    return int(idx), len(l & r)

def solve_p1(lines):
    total = 0
    for line in lines:
        _, c = parse(line)
        if c > 0:
            total += 2 ** (c - 1)
    return total

def solve_p2(lines):
    total = 0
    multi = defaultdict(lambda: 1)
    for line in lines:
        i, c = parse(line)
        for j in range(i + 1, i + 1 + c):
            multi[j] += multi[i]
        total += multi[i]
    return total
