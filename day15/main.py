def parse(lines):
    return ''.join(lines).split(',')

def holiday_hash(s):
    v = 0
    for c in s:
        v = (v + ord(c)) * 17 % 256
    return v

def solve_p1(lines):
    return sum(map(holiday_hash, parse(lines)))

def solve_p2(lines):
    boxes = [{} for _ in range(256)]
    for step in parse(lines):
        if step.endswith('-'):
            label = step[:-1]
            boxes[holiday_hash(label)].pop(label, None)
        else:
            label, focus = step.split('=')
            boxes[holiday_hash(label)][label] = int(focus)
    total = 0
    for box_idx, box in enumerate(boxes, start=1):
        for lens_idx, focus in enumerate(box.values(), start=1):
            total += box_idx * lens_idx * focus
    return total
