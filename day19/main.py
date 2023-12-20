CMP = 0
GOTO = 1
KEYS = 'xmas'

class NormalItem:
    def __init__(self, values):
        self.values = values

    def process(self, rules):
        for rule in rules:
            if rule[0] == GOTO:
                yield self, rule[1]
            elif rule[0] == CMP:
                key, cmp, value, goto = rule[1:]
                rating = self.values[key]
                if (cmp == '>' and rating > value) or (cmp == '<' and rating < value):
                    yield self, goto
                    break

    def score(self):
        return sum(self.values.values())

class QuantumItem:
    def __init__(self, values=None):
        self.values = {key: (1, 4001) for key in range(len(KEYS))} if values is None else values

    def with_range(self, key, value):
        return QuantumItem({**self.values, key: value})

    @staticmethod
    def slice(r, c, v):
        # returns positive branch followed by negative branch as a 2-tuple of [) ranges
        # NB: ranges are adjusted to include v in negative branch result
        if c == '>':
            return (max(v + 1, r[0]), r[1]), (r[0], min(v + 1, r[1]))
        return (r[0], min(v, r[1])), (max(v, r[0]), r[1])

    def process(self, rules):
        remaining = self
        for rule in rules:
            if remaining.score() == 0:
                break
            if rule[0] == GOTO:
                yield remaining, rule[1]
                break
            elif rule[0] == CMP:
                key, cmp, value, goto = rule[1:]
                passed, failed = QuantumItem.slice(remaining.values[key], cmp, value)
                remaining = remaining.with_range(key, failed)
                yield remaining.with_range(key, passed), goto

    def score(self):
        product = 1
        for r in self.values.values():
            if r[0] >= r[1]:
                return 0
            product *= r[1] - r[0]
        return product

def parse_rule(rule):
    if ':' in rule:
        condition, outcome = rule.split(':')
        op_char = '>' if '>' in condition else '<'
        key, value = condition.split(op_char)
        return CMP, KEYS.index(key), op_char, int(value), outcome
    return GOTO, rule

def parse(lines):
    workflows = {}
    items = []
    for line in lines:
        if line.startswith('{'):
            values = [x.split('=') for x in line.strip('{}').split(',')]
            item = {KEYS.index(k): int(v) for k, v in values}
            items.append(NormalItem(item))
        elif line.endswith('}'):
            name, rules = line[:-1].split('{')
            rules = list(map(parse_rule, rules.split(',')))
            workflows[name] = rules
    return workflows, items

def score(item, workflows, start='in', accept='A', reject='R'):
    edge = {(item, start)}
    total = 0
    while edge:
        item, workflow = edge.pop()
        if workflow == accept:
            total += item.score()
        elif workflow != reject:
            for entry in item.process(workflows[workflow]):
                edge.add(entry)
    return total

def solve_p1(lines):
    workflows, items = parse(lines)
    return sum(score(item, workflows) for item in items)

def solve_p2(lines):
    workflows, _ = parse(lines)
    return score(QuantumItem(), workflows)
