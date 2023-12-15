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
    count = [0 for _ in range(256)]
    boxes = [{} for _ in range(256)]
    for step in parse(lines):
        if step.endswith('-'):
            label = step[:-1]
            hh = holiday_hash(label)
            boxes[hh].pop(label, None)
        else:
            label, focus = step.split('=')
            hh = holiday_hash(label)
            box = boxes[hh]
            if label in box:
                box[label][1] = int(focus)
            else:
                box[label] = [count[hh], int(focus)]
                count[hh] += 1
    total = 0
    for box_idx, box in enumerate(boxes, start=1):
        for (len_idx, (_, focus)) in enumerate(sorted(box.values(), key=lambda cf: cf[0]), start=1):
            total += box_idx * len_idx * focus
    return total
