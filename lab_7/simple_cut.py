import copy


def count_S(T):
    return sum(T)


def count_P(T1, T2):
    P = 0
    for i in range(len(T1)):
        P += (T1[i] * T2[i])
    return P


def count_T(p, xl, xr, yd, yu):
    x = p[0]
    y = p[1]
    T = [0, 0, 0, 0]
    T[0] = 1 if x < xl else 0
    T[1] = 1 if x > xr else 0
    T[2] = 1 if y < yd else 0
    T[3] = 1 if y > yu else 0
    return T


def sort_cutter(arr):
    if arr[0][0] > arr[1][0]:
        arr[0], arr[1] = arr[1], arr[0]
    return arr


def easy_cut(xl, xr, yd, yu, p1, p2):
    T1 = count_T(p1, xl, xr, yd, yu)
    T2 = count_T(p2, xl, xr, yd, yu)

    FL = 0
    m = 99999  # Infinity

    S1 = count_S(T1)
    S2 = count_S(T2)

    Q = p1
    r1 = copy.deepcopy(p1)
    r2 = copy.deepcopy(p2)

    if (S1 == 0) and (S2 == 0):
        return B_shtrih(FL, r1, r2)

    P = count_P(T1, T2)
    if P != 0:
        return B(r1, r2)

    if S1 == 0:
        r1 = copy.deepcopy(p1)
        Q = copy.deepcopy(p2)
        i = 2
        return A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu, False)

    if S2 == 0:
        r1 = copy.deepcopy(p2)
        Q = copy.deepcopy(p1)
        i = 2
        return A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu, False)

    i = 0
    return A(FL, i, Q, p1, p2, r1, r2, xl, xr, yd, yu)


def B_shtrih(FL, p1, p2):
    if FL == 0:
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
