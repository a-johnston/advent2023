import re

def _numeric_helper(line):
    numeric = list(filter(str.isnumeric, line))
    return int(numeric[0] + numeric[-1])

def solve_p1(lines):
    return sum(map(_numeric_helper, lines))

# Here marks the spot where I mistyped "seven" as "sevel" and spent an hour angrily debugging
_pattern = re.compile(r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))')

_digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def solve_p2(lines):
    total = 0
    for line in lines:
        groups = _pattern.findall(line)
        digits = [_digits.get(group, group) for group in _pattern.findall(line)]
        total += int(digits[0] + digits[-1])
    return total
