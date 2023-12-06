def parse(lines):
    raw = '\n'.join(lines).split('\n\n')
    seeds = None
    data = {}
    for line in raw:
        k, v = line.split(':')
        v = v.strip()
        if ' map' in k:
            k = k[:-len(' map')]
            v = [[int(y) for y in x.split()] for x in v.split('\n')]
            # return data as sorted [(range start, range end, map delta)..]
            v = sorted((src, src + n, dst - src) for (dst, src, n) in v)
            data[k] = v
        else:
            seeds = list(map(int, v.split()))
    return seeds, data

def find_key_traversal(data, src, dst):
    for k in data:
        if '-to-' in k:
            l, r = k.split('-to-')
            if r == dst:
                return [k]
            if l == src:
                v = find_key_traversal(data, r, dst)
                if v:
                    return [k] + v
    return None

def apply_mapping(x, mapping):
    for start, end, delta in mapping:
        if x < start:
            return x
        if x < end:
            return x + delta
    return x

def apply_range_mapping(seed_range, mapping):
    rs, re = seed_range
    for start, end, delta in mapping:
        if rs < start:
            if re <= start:
                # Entire range is below remaining mapping
                yield (rs, re)
                break
            # Range starts below but overlaps mapping
            yield (rs, start)
            yield from apply_range_mapping((start, re), mapping)
            break
        if rs < end:
            if re <= end:
                # Entire range is within mapping
                yield (rs + delta, re + delta)
                break
            # Range starts within mapping but ends above
            yield (rs + delta, end + delta)
            yield from apply_range_mapping((end, re), mapping)
            break
    else:
        # Entire range is above mapping
        yield (rs, re)

def solve_p1(lines):
    values, data = parse(lines)
    for k in find_key_traversal(data, 'seed', 'location'):
        values = [apply_mapping(x, data[k]) for x in values]
    return min(values)

def solve_p2(lines):
    values, data = parse(lines)
    values = [(values[i], values[i] + values[i + 1]) for i in range(0, len(values), 2)]
    for k in find_key_traversal(data, 'seed', 'location'):
        new_values = []
        for x in values:
            if x[0] == x[1]:
                continue
            new_values.extend(apply_range_mapping(x, data[k]))
        values = new_values
    return min(values)[0]
