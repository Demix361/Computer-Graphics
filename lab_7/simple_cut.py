from copy import deepcopy


def simple_cut(line, cutter):
    p1 = (line.x1, line.y1)
    p2 = (line.x2, line.y2)
    xl = cutter.x_left
    xr = cutter.x_right
    yd = cutter.y_down
    yu = cutter.y_up

    t1 = get_t(p1, cutter)
    t2 = get_t(p2, cutter)
    print(t1, t2)

    fl = 0
    m = 99999  # Infinity

    s1 = get_s(t1)
    s2 = get_s(t2)

    q = deepcopy(p1)
    r1 = deepcopy(p1)
    r2 = deepcopy(p2)

    if s1 == 0 and s2 == 0:
        return B_shtrih(fl, r1, r2)

    p = get_p(t1, t2)
    if p != 0:
        return B(r1, r2)

    if s1 == 0:
        r1 = deepcopy(p1)
        q = deepcopy(p2)
        i = 2
        return A(fl, i, q, p1, p2, r1, r2, xl, xr, yd, yu, False)

    if s2 == 0:
        r1 = deepcopy(p2)
        q = deepcopy(p1)
        i = 2
        return A(fl, i, q, p1, p2, r1, r2, xl, xr, yd, yu, False)

    i = 0
    return A(fl, i, q, p1, p2, r1, r2, xl, xr, yd, yu)


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

# =============================================================================



def B_shtrih(flag, p1, p2):
    if flag == 0:
        return True, p1, p2
    else:
        return False, p1, p2


def B(p1, p2):
    return B_shtrih(1, p1, p2)


def A_skip_1(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu, m):
    if m == 0:
        return B(r1, r2)

    if Q[1] < yd:
        x = (yd - Q[1]) / m + Q[0]

        if xl <= x and x <= xr:
            if i == 1:
                r1[0] = x
                r1[1] = yd
            else:
                r2[0] = x
                r2[1] = yd
            return A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu)

    if Q[1] > yu:
        x = (yu - Q[1]) / m + Q[0]

        if xl <= x and x <= xr:
            if i == 1:
                r1[0] = x
                r1[1] = yu
            else:
                r2[0] = x
                r2[1] = yu
            return A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu)

    return B(r1, r2)


def A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu, flag=True):
    if flag:
        i += 1
        if i > 2:
            return B_shtrih(FL, r1, r2)

        Q = p1 if i == 1 else p2

    if p1[0] == p2[0]:
        return A_skip_1(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu, 99999)

    m = (p2[1] - p1[1]) / (p2[0] - p1[0])

    if Q[0] < xl:
        y = m * (xl - Q[0]) + Q[1]

        if yd <= y and y <= yu:
            if i == 1:
                r1[0] = xl
                r1[1] = y
            else:
                r2[0] = xl
                r2[1] = y
            return A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu)

    if Q[0] > xr:
        y = m * (xr - Q[0]) + Q[1]

        if yd <= y and y <= yu:
            if i == 1:
                r1[0] = xr
                r1[1] = y
            else:
                r2[0] = xr
                r2[1] = y
            return A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu)

    return A_skip_1(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu, m)