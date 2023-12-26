from itertools import combinations

def check_side(v, dv, cv):
    if cv < v:
        return dv < 0
    if cv > v:
        return dv > 0
    return True

def inv(a):
    return -a[0], -a[1], -a[2]

def scale(v, n):
    return v[0] * n, v[1] * n, v[2] * n

def add(a, b):
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]

def sub(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def cross(a, b):
    return a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]

class Stone:
    def __init__(self, idx, pos, vel):
        self.idx = idx
        self.pos = pos
        self.vel = vel

    def get_dets(self):
        x1, y1 = self.pos[0], self.pos[1]
        x2, y2 = x1 + self.vel[0], y1 + self.vel[1]
        return x1 * y2 - x2 * y1, x1 - x2, y1 - y2

    def check_xy(self, px, py):
        return check_side(self.pos[0], self.vel[0], px) and check_side(self.pos[1], self.vel[1], py)

    def get_z(self, px, py):
        r = (px - self.pos[0]) / self.vel[0]
        return self.pos[2] + self.vel[2] * r

    def at(self, t):
        return add(self.pos, scale(self.vel, t))

    def test_intersects_path_2d(self, other, test=None):
        a_xy, a_x, a_y = self.get_dets()
        b_xy, b_x, b_y = other.get_dets()
        pxn = a_xy * b_x - a_x * b_xy
        pyn = a_xy * b_y - a_y * b_xy
        pd = a_x * b_y - a_y * b_x
        if pd == 0:
            return False
        px = pxn / pd
        py = pyn / pd
        if not self.check_xy(px, py) or not other.check_xy(px, py):
            return False
        if test is not None and (px < test[0] or px > test[1] or py < test[0] or py > test[1]):
            return False
        return True

    def intersect_plane(self, n):
        t = dot(inv(self.pos), n) / dot(self.vel, n)
        return self.at(t), t

    def in_frame(self, frame):
        return Stone(self.idx, sub(self.pos, frame.pos), sub(self.vel, frame.vel))

    def out_frame(self, frame):
        return Stone(self.idx, add(self.pos, frame.pos), add(self.vel, frame.vel))

def parse(lines):
    stones = []
    area = tuple(map(int, lines[0].split()))
    for line in lines[1:]:
        l, r = line.split(' @ ')
        l = tuple(map(int, l.split(', ')))
        r = tuple(map(int, r.split(', ')))
        stones.append(Stone(chr(ord('A') + len(stones)), l, r))
    return area, stones

def solve_p1(lines):
    area, stones = parse(lines)
    return sum(a.test_intersects_path_2d(b, area) for a, b in combinations(stones, 2))

def solve_p2(lines):
    _, stones = parse(lines)
    # Use first stone as a frame of reference; thrown rock must cross origin in this frame
    ref = stones[0]
    # Use second stone in above frame to define a plane containing that stone's path and origin
    a = stones[1].in_frame(ref)
    n = cross(a.vel, a.pos)
    # Intersect third and fourth stones with plane to obtain t3 and t4
    i3, t3 = stones[2].in_frame(ref).intersect_plane(n)
    i4, t4 = stones[3].in_frame(ref).intersect_plane(n)
    # Compute throw velocity and then position using obtained points and times
    v = scale(sub(i4, i3), 1 / (t4 - t3))
    p = sub(i3, scale(v, t3))
    return int(sum(Stone(-1, p, v).out_frame(ref).pos))
