from functools import cache

def parse(lines):
    data = []
    for line in lines:
        l, r = line.split()
        data.append((l, tuple(map(int, r.split(',')))))
    return data

def get_possible_starts(block, start=0):
    for i, c in enumerate(block[start:], start=start):
        if c == '#' and (i == 0 or block[i - 1] != '#'):
            yield i
        else:
            if i > 0 and block[i - 1] == '#':
                break
            if c == '?':
                yield i

@cache
def try_place(block, start, count):
    if start + count > len(block):
        return False
    if start + count < len(block) and block[start + count] == '#':
        return False
    for i in range(start, start + count):
        if block[i] == '.':
            return False
    return True

@cache
def count(block, start, counts):
    if len(counts) == 0:
        return 1
    head, rest = counts[0], counts[1:]
    total = 0
    for i in get_possible_starts(block, start):
        if try_place(block, i, head):
            if len(rest) == 0 and block.find('#', i + head) != -1:
                continue
            total += count(block, i + head + 1, rest)
    return total

def get_total(lines, multi):
    total = 0
    for block, counts in parse(lines):
        total += count('?'.join([block] * multi), 0, counts * multi)
    return total

def solve_p1(lines):
    return get_total(lines, 1)

def solve_p2(lines):
    return get_total(lines, 5)
