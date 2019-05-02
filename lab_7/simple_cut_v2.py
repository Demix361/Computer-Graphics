from copy import deepcopy


def simple_cut(line, cutter):
    p1 = (line.x1, line.y1)
    p2 = (line.x2, line.y2)
    xl = cutter.x_left
    xr = cutter.x_right
    yd = cutter.y_down
    yu = cutter.y_up

    step_1()


def get_t(p, cutter):
    x = p[0]
    y = p[1]
    t = [0, 0, 0, 0]

    t[0] = 1 if y < cutter.y_up else 0
    t[1] = 1 if y > cutter.y_down else 0
    t[2] = 1 if x < cutter.x_left else 0
    t[3] = 1 if x > cutter.x_right else 0

    return t


def get_s(t):
    return sum(t)


def get_p(t1, t2):
    p = 0

    for i in range(len(t1)):
        p += t1[i] * t2[i]

    return p


def step_1(p1, p2, cutter):
    t1 = get_t(p1, cutter)
    t2 = get_t(p2, cutter)

    s1 = get_s(t1)
    s2 = get_s(t2)

    vis = 1

    m = 99999

    if s1 == 0 and s2 == 0:
        r1 = deepcopy(p1)
        r2 = deepcopy(p2)

        step_31(vis, r1, r2)

    p = get_p(t1, t2)

    if p == 0:
        vis = 0
        r1 = deepcopy(p1)
        r2 = deepcopy(p2)

        step_31(vis, r1, r2)

    if s1 == 0:
        r1 = deepcopy(p1)
        q = deepcopy(p2)
        i = 2

        step_15()

    if s2 == 0:
        r1 = deepcopy(p2)
        q = deepcopy(p1)
        i = 2

        step_15()

    i = 0

    step_12(i, vis, r1, r2, p1, p2)


def step_12(i, vis, r1, r2, p1, p2):
    i += 1

    if i > 2:
        step_31(vis, r1, r2)

    if i == 1:
        q = deepcopy(p1)
    elif i == 2:
        q = deepcopy(p2)

    step_15()


def step_15(p1, p2, cutter, r1, r2, i):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    if x1 == x2:
        step_23()

    m = (y2 - y1) / (x2 - x1)

    if q[0] > cutter.x_left:
        step_20()

    y_cross = m * (cutter.x_left - q[0]) + q[1]

    if cutter.y_down < y_cross < cutter.y_up:
        if i == 1:
            r1[0] = cutter.x_left
            r1[1] = y_cross
        elif i == 2:
            r2[0] = cutter.x_left
            r2[1] = y_cross




