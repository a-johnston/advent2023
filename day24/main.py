import z3

def get_2d_dets(pos, vel):
    x1, y1 = pos[0], pos[1]
    x2, y2 = x1 + vel[0], y1 + vel[1]
    return x1 * y2 - x2 * y1, x1 - x2, y1 - y2

def check_side(v, dv, cv):
    if cv < v:
        return dv < 0
    if cv > v:
        return dv > 0
    return True

def inv(a):
    return -a[0], -a[1], -a[2]

def length(v):
    return (dot(v, v)) ** 0.5

def scale(v, n):
    return v[0] * n, v[1] * n, v[2] * n

def norm(v):
    return scale(v, 1 / length(v))

def add(a, b):
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]

def sub(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] + b[2]

def cross(a, b):
    return a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]

class Stone:
    def __init__(self, idx, pos, vel):
        self.idx = idx
        self.pos = pos
        self.vel = vel
        self.dets = get_2d_dets(pos, vel)

    def check_xy(self, px, py):
        return check_side(self.pos[0], self.vel[0], px) and check_side(self.pos[1], self.vel[1], py)

    def get_z(self, px, py):
        r = (px - self.pos[0]) / self.vel[0]
        return self.pos[2] + self.vel[2] * r

    def at(self, t):
        return add(self.pos, scale(self.vel, t))

    def in_frame(self, frame):
        return Stone(self.idx, sub(frame.pos, self.pos), sub(frame.vel, self.vel))

    def out_frame(self, frame):
        return Stone(self.idx, add(frame.pos, self.pos), add(frame.vel, self.vel))

def parse(lines):
    stones = []
    area = tuple(map(int, lines[0].split()))
    for line in lines[1:]:
        l, r = line.split(' @ ')
        l = tuple(map(int, l.split(', ')))
        r = tuple(map(int, r.split(', ')))
        stones.append(Stone(chr(ord('A') + len(stones)), l, r))
    return area, stones

def get_intersection(a, b):
    a_xy, a_x, a_y = a.dets
    b_xy, b_x, b_y = b.dets
    pxn = a_xy * b_x - a_x * b_xy
    pyn = a_xy * b_y - a_y * b_xy
    pd = a_x * b_y - a_y * b_x
    if pd == 0:
        return None, None
    px = pxn / pd
    py = pyn / pd
    if not a.check_xy(px, py) or not b.check_xy(px, py):
        return None, None
    return px, py

def solve_p1(lines):
    area, stones = parse(lines)
    count = 0
    for i, a in enumerate(stones):
        for b in stones[i:]:
            ix, iy = get_intersection(a, b)
            if ix is None:
                continue
            if ix < area[0] or ix > area[1] or iy < area[0] or iy > area[1]:
                continue
            count += 1
    return count

def intersect_plane(n, stone):
    t = dot(inv(stone.pos), n) / dot(stone.vel, n)
    return stone.at(t), t

def solve_p2(lines):
    _, stones = parse(lines)
    # Use first stone as a frame of reference; thrown rock must cross origin in this frame
    ref = stones[0]
    # Use second stone in above frame to define a plane containing that stone and zero
    a = stones[1].in_frame(ref)
    n = cross(a.vel, inv(a.pos))
    # Intersect third and fourth stones with plane to obtain t3 and t4
    i3, t3 = intersect_plane(n, stones[3].in_frame(ref))
    i4, t4 = intersect_plane(n, stones[4].in_frame(ref))
    # Compute throw velocity and then position using obtained points and times
    v = scale(sub(i4, i3), 1 / (t4 - t3))
    p = sub(i3, scale(v, t3))
    return add(p, ref.pos)

def solve_p3(lines):
    _, stones = parse(lines)

    rx, ry, rz = z3.Reals('rx ry rz')
    rvx, rvy, rvz = z3.Reals('rvx rvy rvz')
    t0, t1, t2 = z3.Reals('t0 t1 t2')
    answer = z3.Real('answer')

    a, b, c = stones[0], stones[1], stones[2]

    return z3.solve(
        # Stone 0
        rx + t0 * rvx == a.pos[0] + t0 * a.vel[0],
        ry + t0 * rvy == a.pos[1] + t0 * a.vel[1],
        rz + t0 * rvz == a.pos[2] + t0 * a.vel[2],
        # Stone 1
        rx + t1 * rvx == b.pos[0] + t1 * b.vel[0],
        ry + t1 * rvy == b.pos[1] + t1 * b.vel[1],
        rz + t1 * rvz == b.pos[2] + t1 * b.vel[2],
        # Stone 2
        rx + t2 * rvx == c.pos[0] + t2 * c.vel[0],
        ry + t2 * rvy == c.pos[1] + t2 * c.vel[1],
        rz + t2 * rvz == c.pos[2] + t2 * c.vel[2],
        # Result
        answer == rx + ry + rz
    )
