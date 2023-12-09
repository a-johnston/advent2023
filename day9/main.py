def get_next(seq):
    subseq = []
    for i in range(1, len(seq)):
        subseq.append(seq[i] - seq[i - 1])
    v = get_next(subseq) if any(s != 0 for s in subseq) else 0
    return seq[-1] + v

def solve_p1(lines):
    total = 0
    for line in lines:
        total += get_next(list(map(int, line.split())))
    return total

def solve_p2(lines):
    total = 0
    for line in lines:
        total += get_next(list(map(int, reversed(line.split()))))
    return total
