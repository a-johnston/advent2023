def parse(lines):
    patterns = []
    pattern = []
    for line in (lines + ['']):
        if len(line) == 0 and len(pattern) > 0:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line.replace('#', '1').replace('.', '0'))
    return patterns

def transpose(pattern):
    return [''.join(x) for x in zip(*pattern)]

def count_mirrored_rows(pattern, allowed_smudges):
    vals = [int(x, 2) for x in pattern]
    for split in range(1, len(pattern)):
        smudge_factor = 0
        for i, j in zip(range(split - 1, -1, -1), range(split, len(pattern))):
            smudge_factor += (vals[i] ^ vals[j]).bit_count()
            if smudge_factor > allowed_smudges:
                break
        if smudge_factor == allowed_smudges:
            return split
    return 0

def count(pattern, allowed_smudges):
    x = count_mirrored_rows(pattern, allowed_smudges)
    if x > 0:
        return 100 * x
    return count_mirrored_rows(transpose(pattern), allowed_smudges)

def solve_p1(lines):
    return sum(count(pattern, 0) for pattern in parse(lines))

def solve_p2(lines):
    return sum(count(pattern, 1) for pattern in parse(lines))
