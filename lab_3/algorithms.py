from PyQt5.QtGui import QColor


def drawline_std(bg, x1, y1, x2, y2):
    bg.drawLine(x1, y1, x2, y2)


def drawline_dda(can, x1, y1, x2, y2):
    len_x = abs(int(x2) - int(x1))
    len_y = abs(int(y2) - int(y1))

    if len_x == 0 and len_y == 0:
        can.drawPoint(x1, y1)
        return 1

    n = max(len_x, len_y)

    dx = ((x2 > x1) - (x2 < x1)) * len_x / n
    dy = ((y2 > y1) - (y2 < y1)) * len_y / n

    for i in range(n + 1):
        can.drawPoint(int(x1), int(y1))
        x1 += dx
        y1 += dy

    return 0


def drawline_br_float(can, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        can.drawPoint(x1, x2)
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
        can.drawPoint(x, y)
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


def drawline_br_int(can, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        can.drawPoint(x1, x2)
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
        can.drawPoint(x1, y1)
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


def drawline_br_smooth(can, x1, y1, x2, y2, line_color, bg_color):
    dx = x2 - x1
    dy = y2 - y1
    i_max = 1
    x = x1
    y = y1

    if dx == 0 and dy == 0:
        can.drawPoint(x1, x2)
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
        can.setPen(QColor(line_color[0] + e * d_r, line_color[1] + e * d_g, line_color[2] + e * d_b))
        can.drawPoint(x, y)

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


def drawline_wu(can, x1, y1, x2, y2, line_color, bg_color):
    if x1 == x2 and y1 == y2:
        can.drawPoint(x1, y1)
        return 1

    if int(x2) - int(x1) == 0:
        can.drawLine(x1, y1, x2, y2)
        return 2

    if int(y2) - int(y1) == 0:
        can.drawLine(x1, y1, x2, y2)
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
        change_color(can, line_color, bg_color, 1)
        can.drawPoint(ypx1, xpx1)
        change_color(can, line_color, bg_color, fpart(yend) * xgap)
        can.drawPoint(ypx1, xpx1 + 1)
    else:
        change_color(can, line_color, bg_color, 1)
        can.drawPoint(xpx1, ypx1)
        change_color(can, line_color, bg_color, fpart(yend) * xgap)
        can.drawPoint(xpx1, ypx1 + 1)

    intery = yend + grad

    # second endpoint
    xend = int(x2 + 0.5)
    xpx2 = xend

    # main loop
    if steep:
        for x in range(xpx1, xpx2):
            change_color(can, line_color, bg_color, 1 - (intery - int(intery)))
            can.drawPoint(int(intery), x + 1)
            change_color(can, line_color, bg_color, intery - int(intery))
            can.drawPoint(int(intery) + 1, x + 1)
            intery += grad
    else:
        for x in range(xpx1, xpx2):
            change_color(can, line_color, bg_color, 1 - (intery - int(intery)))
            can.drawPoint(x + 1, int(intery))
            change_color(can, line_color, bg_color, intery - int(intery))
            can.drawPoint(x + 1, int(intery) + 1)
            intery += grad

    return 0


def change_color(can, line_color, bg_color, intensity):
    intensity = 1 - intensity

    dr = bg_color[0] - line_color[0]
    dg = bg_color[1] - line_color[1]
    db = bg_color[2] - line_color[2]

    new_color = QColor(line_color[0] + dr * intensity, line_color[1] + dg * intensity, line_color[2] + db * intensity)

    can.setPen(new_color)


def fpart(x):
    return x - int(x)


def rfpart(x):
    return 1 - fpart(x)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
