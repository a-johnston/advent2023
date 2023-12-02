def parse_helper(items):
    return {color: int(val) for val, color in items}

def parse(line):
    l, r = line.split(': ')
    game_id = int(l.split(' ')[1])
    rounds = [
        parse_helper([y.split(' ') for y in x.split(', ')])
        for x in r.split('; ')
    ]
    return (game_id, rounds)

def compare(group, limit):
    for k, v in group.items():
        if v > limit[k]:
            return False
    return True

def solve_p1(lines):
    limits = {'red': 12, 'green': 13, 'blue': 14}
    total = 0
    for line in lines:
        game_id, groups = parse(line)
        if all(compare(group, limits) for group in groups):
            total += game_id
    return total

def min_helper(a, b):
    for k, v in b.items():
        a[k] = max(v, a.get(k, v))

def product(args):
    val = 1
    for a in args:
        val *= a
    return val

def solve_p2(lines):
    total = 0
    for line in lines:
        mins = {}
        game_id, groups = parse(line)
        for group in groups:
            min_helper(mins, group)
        total += product(mins.values())
    return total
