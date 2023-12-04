def add_filler(lines):
    lines = [f'.{line}.' for line in lines]
    filler = '.' * len(lines[0])
    lines.insert(0, filler)
    lines.append(filler)
    return lines

def is_near_symbol(lines, i, j):
    for ii in range(i - 1, i + 2):
        for jj in range(j - 1, j + 2):
            c = lines[ii][jj]
            if not c.isnumeric() and c != '.':
                return True
    return False

def solve_p1(lines):
    lines = add_filler(lines)
    total = 0
    run = ''
    near_symbol = False
    for i in range(1, len(lines) - 1):
        line = lines[i]
        for j, c in enumerate(line):
            if c.isnumeric():
                run += c
                if is_near_symbol(lines, i, j):
                    near_symbol = True
            else:
                if run and near_symbol:
                    total += int(run)
                run = ''
                near_symbol = False
    return total

def try_scan_number(line, i):
    run = line[i]
    for j in range(i - 1, 0, -1):
        if line[j].isnumeric():
            run = line[j] + run
        else:
            break
    for j in range(i + 1, len(line)):
        if line[j].isnumeric():
            run += line[j]
        else:
            break
    if run.isnumeric():
        return int(run)
    return -1

def try_get_gear_ratio(lines, i, j):
    values = []
    last = -1
    for ii in range(i - 1, i + 2):
        for jj in range(j - 1, j + 2):
            gear = try_scan_number(lines[ii], jj)
            if gear != -1 and gear != last:
                values.append(gear)
            last = gear
    if len(values) == 2:
        return values[0] * values[1]
    return 0

def solve_p2(lines):
    lines = add_filler(lines)
    total = 0
    for i in range(1, len(lines) - 1):
        line = lines[i]
        for j, c in enumerate(line):
            if c == '*':
                total += try_get_gear_ratio(lines, i, j)
    return total
