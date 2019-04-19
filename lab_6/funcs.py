def draw_pix(self, x, y, color):
    self.image.setPixel(x, y, color.rgb())


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def create_line(self, dot1, dot2):
    x1, y1 = dot1
    x2, y2 = dot2

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        draw_pix(self, x1, y1, self.bd_color)
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
        draw_pix(self, x1, y1, self.bd_color)
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
