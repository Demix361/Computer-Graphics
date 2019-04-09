from PyQt5.QtGui import QColor
from algorithms import sign, fpart


def change_color(line_color, bg_color, intensity):
    intensity = 1 - intensity

    dr = bg_color[0] - line_color[0]
    dg = bg_color[1] - line_color[1]
    db = bg_color[2] - line_color[2]

    new_color = QColor(dr * intensity, dg * intensity, db * intensity)

    return 0


#=====TIME MEASURE=====
def test_dda(x1, y1, x2, y2):
    len_x = abs(int(x2) - int(x1))
    len_y = abs(int(y2) - int(y1))

    if len_x == 0 and len_y == 0:
        # draw pix
        return 1

    n = max(len_x, len_y)

    dx = ((x2 > x1) - (x2 < x1)) * len_x / n
    dy = ((y2 > y1) - (y2 < y1)) * len_y / n

    for i in range(n + 1):
        # draw pix
        x1 = int(x1)
        y1 = int(y1)
        x1 += dx
        y1 += dy

    return 0


def test_br_float(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        # draw pix
        return 1

    x = x1
    y = y1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx

    m = dy / dx
    e = m - 0.5

    while x != x2 or y != y2:
        # draw pix
        if e >= 0:
            if change == 0:
                y += sy
            else:
                x += sx
            e -= 1
        if e < 0:
            if change == 0:
                x += sx
            else:
                y += sy
            e += m

    return 0


def test_br_int(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        # draw pix
        return 1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx

    e = 2 * dy - dx
    new_dx = 2 * dx
    new_dy = dy * 2
    
    while x1 != x2 or y1 != y2:
        # draw pix
        if e >= 0:
            if change == 0:
                y1 += sy
            else:
                x1 += sx
            e -= new_dx
        if e < 0:
            if change == 0:
                x1 += sx
            else:
                y1 += sy
            e += new_dy

    return 0


def test_br_smooth(x1, y1, x2, y2, line_color, bg_color):
    dx = x2 - x1
    dy = y2 - y1
    i_max = 1
    x = x1
    y = y1

    if dx == 0 and dy == 0:
        # draw pix
        return 1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    try:
        m = dy / dx
    except ZeroDivisionError:
        m = 0

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx
        if m:
            m = 1 / m

    m *= i_max
    e = i_max / 2
    w = i_max - m

    d_r = bg_color[0] - line_color[0]
    d_g = bg_color[1] - line_color[1]
    d_b = bg_color[2] - line_color[2]
    i = 1
    while i <= dx:
        new_color = QColor(line_color[0] + e * d_r, line_color[1] + e * d_g, line_color[2] + e * d_b)
        # draw pix

        if e <= w:
            if change == 0:
                x += sx
            else:
                y += sy
            e += m
        else:
            x += sx
            y += sy
            e -= w
        i += 1

    return 0


def test_wu(x1, y1, x2, y2, line_color, bg_color):
    if x1 == x2 and y1 == y2:
        # draw pix
        return 1

    if int(x2) - int(x1) == 0:
        # draw line
        return 2

    if int(y2) - int(y1) == 0:
        # draw line
        return 3

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        grad = 1
    else:
        grad = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + grad * (xend - x1)
    xgap = 1 - ((x1 + 0.5) - int(x1 + 0.5))
    xpx1 = xend
    ypx1 = int(yend)

    if steep:
        change_color(line_color, bg_color, 1)
        # draw pix
        change_color(line_color, bg_color, fpart(yend) * xgap)
        # draw pix
    else:
        change_color(line_color, bg_color, 1)
        # draw pix
        change_color(line_color, bg_color, fpart(yend) * xgap)
        # draw pix

    intery = yend + grad

    # second endpoint
    xend = int(x2 + 0.5)
    xpx2 = xend

    # main loop
    if steep:
        for x in range(xpx1, xpx2):
            change_color(line_color, bg_color, 1 - (intery - int(intery)))
            # draw pix
            change_color(line_color, bg_color, intery - int(intery))
            # draw pix
            intery += grad
    else:
        for x in range(xpx1, xpx2):
            change_color(line_color, bg_color, 1 - (intery - int(intery)))
            # draw pix
            change_color(line_color, bg_color, intery - int(intery))
            # draw pix
            intery += grad


# =====STEP MEASURE=====
def step_dda(x1, y1, x2, y2):
    len_x = abs(int(x2) - int(x1))
    len_y = abs(int(y2) - int(y1))

    if len_x == 0 and len_y == 0:
        return 1

    n = max(len_x, len_y)

    dx = ((x2 > x1) - (x2 < x1)) * len_x / n
    dy = ((y2 > y1) - (y2 < y1)) * len_y / n

    steep = abs(y2 - y1) > abs(x2 - x1)

    cur_x = int(x1)
    cur_y = int(y1)
    max_step = 0
    cur_step = 0

    for i in range(n + 1):
        if steep:
            if int(x1) != cur_x:

                cur_step = 1
                cur_x = int(x1)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step
        else:
            if int(y1) != cur_y:

                cur_step = 1
                cur_y = int(y1)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step

        x1 += dx
        y1 += dy

    return max_step


def step_br_float(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return 1

    x = x1
    y = y1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx

    m = dy / dx
    e = m - 0.5

    cur_x = x
    cur_y = y
    cur_step = 0
    max_step = 0

    while x != x2 or y != y2:
        if change:
            if int(x) != cur_x:
                cur_step = 1
                cur_x = int(x)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step
        else:
            if int(y) != cur_y:
                cur_step = 1
                cur_y = int(y)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step

        if e >= 0:
            if change == 0:
                y += sy
            else:
                x += sx
            e -= 1
        if e < 0:
            if change == 0:
                x += sx
            else:
                y += sy
            e += m

    return max_step


def step_br_int(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return 1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx

    e = 2 * dy - dx

    cur_x = x1
    cur_y = y1
    cur_step = 0
    max_step = 0

    while x1 != x2 or y1 != y2:
        if change:
            if int(x1) != cur_x:
                cur_step = 1
                cur_x = int(x1)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step
        else:
            if int(y1) != cur_y:
                cur_step = 1
                cur_y = int(y1)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step

        if e >= 0:
            if change == 0:
                y1 += sy
            else:
                x1 += sx
            e -= 2 * dx
        if e < 0:
            if change == 0:
                x1 += sx
            else:
                y1 += sy
            e += 2 * dy

    return max_step


def step_br_smooth(x1, y1, x2, y2, line_color, bg_color):
    dx = x2 - x1
    dy = y2 - y1
    i_max = 1
    x = x1
    y = y1

    if dx == 0 and dy == 0:
        return 1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    try:
        m = dy / dx
    except ZeroDivisionError:
        m = 0

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx
        if m:
            m = 1 / m

    m *= i_max
    e = i_max / 2
    w = i_max - m

    d_r = bg_color[0] - line_color[0]
    d_g = bg_color[1] - line_color[1]
    d_b = bg_color[2] - line_color[2]
    i = 1

    cur_x = x1
    cur_y = y1
    cur_step = 0
    max_step = 0

    while i <= dx:
        new_color = QColor(line_color[0] + e * d_r, line_color[1] + e * d_g, line_color[2] + e * d_b)

        if change:
            if int(x) != cur_x:
                cur_step = 1
                cur_x = int(x)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step
        else:
            if int(y) != cur_y:
                cur_step = 1
                cur_y = int(y)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step

        if e <= w:
            if change == 0:
                x += sx
            else:
                y += sy
            e += m
        else:
            x += sx
            y += sy
            e -= w
        i += 1

    return max_step


def step_wu(x1, y1, x2, y2, line_color, bg_color):
    if x1 == x2 and y1 == y2:
        return 1

    if int(x2) - int(x1) == 0:
        return 1

    if int(y2) - int(y1) == 0:
        return abs(int(x2) - int(x1)) + 1

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        grad = 1
    else:
        grad = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + grad * (xend - x1)
    xgap = 1 - ((x1 + 0.5) - int(x1 + 0.5))
    xpx1 = xend
    ypx1 = int(yend)

    if steep:
        change_color(line_color, bg_color, 1)
        #
        change_color(line_color, bg_color, fpart(yend) * xgap)
        #
    else:
        change_color(line_color, bg_color, 1)
        #
        change_color(line_color, bg_color, fpart(yend) * xgap)
        #

    intery = yend + grad

    # second endpoint
    xend = int(x2 + 0.5)
    yend = y2 + grad * (xend - x2)
    xgap = (x2 + 0.5) - int(x2 + 0.5)
    xpx2 = xend
    ypx2 = int(yend)

    cur_x = x1
    cur_y = y1
    cur_step = 0
    max_step = 0

    # main loop
    if steep:
        for x in range(xpx1, xpx2):
            if int(intery) != cur_x:
                cur_step = 1
                cur_x = int(intery)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step

            change_color(line_color, bg_color, 1 - (intery - int(intery)))
            #
            change_color(line_color, bg_color, intery - int(intery))
            #
            intery += grad
    else:
        for x in range(xpx1, xpx2):
            if int(intery) != cur_y:
                cur_step = 1
                cur_y = int(intery)
            else:
                cur_step += 1
                if cur_step > max_step:
                    max_step = cur_step

            change_color(line_color, bg_color, 1 - (intery - int(intery)))
            #
            change_color(line_color, bg_color, intery - int(intery))
            #
            intery += grad

    return max_step
