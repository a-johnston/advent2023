from math import lcm

FLIPFLOP = '%'
CONJUNCTION = '&'
BROADCASTER = ''
TEST = 'T'

def parse(lines):
    modules = {}
    # Create module data
    for line in lines:
        l, r = line.split(' -> ')
        outputs = r.split(', ')
        if l.startswith(FLIPFLOP):
            modules[l[1:]] = [FLIPFLOP, [False], outputs, [], None]
        elif l.startswith(CONJUNCTION):
            modules[l[1:]] = [CONJUNCTION, {}, outputs, [], None]
        else:
            modules[l] = [BROADCASTER, None, outputs, [], None]
    # Assign input connections and create test modules
    for name, data in list(modules.items()):
        for connection in data[2]:
            if connection not in modules:
                modules[connection] = [TEST, None, None, [], None]
            modules[connection][3].append(name)
    # Initialize conjunction state
    for name, data in modules.items():
        if data[0] == CONJUNCTION:
            for input_name in data[3]:
                data[1][input_name] = False
    return modules

def count_signal(modules, start='broadcaster', send=False, origin='button', track=None):
    edge = [(start, send, origin)]
    counts = [0, 0]
    while edge:
        name, signal, sender = edge.pop(0)
        counts[signal] += 1
        module, state, out_con, in_con, last = modules[name]
        output = None
        if module == TEST:
            continue
        elif module == FLIPFLOP:
            if not signal:
                state[0] = not state[0]
                output = state[0]
        elif module == CONJUNCTION:
            state[sender] = signal
            output = not all(state.values())
        else:
            output = signal
        if output is not None:
            modules[name][-1] = output
            for connection in out_con:
                edge.append((connection, output, name))
        if track and name in track and output != last:
            track[name] = True
    return counts

def solve_p1(lines):
    modules = parse(lines)
    lo_total, hi_total = 0, 0
    for _ in range(1000):
        lo, hi = count_signal(modules)
        lo_total += lo
        hi_total += hi
        pass
    return lo_total * hi_total

def find_suspicious_conjunctions(modules, start):
    sus = set()
    edge = {start}
    while edge:
        name = edge.pop()
        module = modules[name]
        if any(modules[con][0] == FLIPFLOP for con in module[3]):
            sus.add(name)
        else:
            for con in module[3]:
                edge.add(con)
    return sus

def solve_p2(lines):
    modules = parse(lines)
    keys = find_suspicious_conjunctions(modules, 'rx')
    track = {key: None for key in keys}
    index = {key: 0 for key in keys}
    rounds = 0
    while any(x < 2 for x in index.values()):
        count_signal(modules, track=track)
        rounds += 1
        for name in track:
            if track[name] and rounds > 1:
                index[name] = rounds
            track[name] = False
    return lcm(*index.values())
