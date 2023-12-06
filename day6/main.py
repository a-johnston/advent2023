import math

def parse(lines):
    columns = zip(*(line.split() for line in lines))
    headers = [x[:-1].lower() for x in next(columns)]
    return [dict(zip(headers, map(int, col))) for col in columns]

def quad_race(time, distance):
    sqrt_term = time ** 2 - 4 * distance
    if sqrt_term < 0:
        return 1
    x = (time + sqrt_term ** 0.5) / 2
    y = (time - sqrt_term ** 0.5) / 2
    x = int(x - 1 if x == int(x) else math.floor(x))
    y = int(y + 1 if y == int(y) else math.ceil(y))
    return x - y + 1

def solve_p1(lines):
    data = parse(lines)
    total = 1
    for race in data:
        total *= quad_race(**race)
    return total

def solve_p2(lines):
    return solve_p1(line.replace(' ', '').replace(':', ': ') for line in lines)
