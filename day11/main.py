def cumulative(vals, to, offset):
    v = 0
    l = [0] * to
    for i in range(to):
        if i in vals:
            v += offset
        l[i] = v
    return l

def parse(lines, offset):
    galaxies = []
    empty_x = set(range(len(lines[0])))
    empty_y = set(range(len(lines)))
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                if x in empty_x:
                    empty_x.remove(x)
                if y in empty_y:
                    empty_y.remove(y)
                galaxies.append([x, y])
    offset_x = cumulative(empty_x, len(lines[0]), offset)
    offset_y = cumulative(empty_y, len(lines), offset)
    for galaxy in galaxies:
        galaxy[0] += offset_x[galaxy[0]]
        galaxy[1] += offset_y[galaxy[1]]
    return galaxies

def find_lengths(galaxies):
    total = 0
    for a in galaxies:
        for b in galaxies:
            if a == b:
                continue
            total += abs(a[0] - b[0]) + abs(a[1] - b[1])
    return int(total / 2)

def solve_p1(lines):
    return find_lengths(parse(lines, 1))

def solve_p2(lines):
    return find_lengths(parse(lines, 999999))
