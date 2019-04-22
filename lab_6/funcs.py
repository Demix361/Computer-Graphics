from PyQt5.QtWidgets import QApplication


# Закрашивает пиксель цветом
def put_pix(self, x, y, color):
    self.image.setPixel(x, y, color.rgb())


# Возвращает цвет пикселя
def get_pix(self, x, y):
    return self.image.pixelColor(x, y)


# Рисует линию целочисленным Брезенхемомом
def create_line(self, dot1, dot2):
    x1, y1 = dot1
    x2, y2 = dot2

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        put_pix(self, x1, y1, self.bd_color)
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
        put_pix(self, x1, y1, self.bd_color)
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


# Оценка знака числа
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# Рисует границы вокруг полотна указанным цветом
def put_borders(self, color):
    for i in range(self.can_w):
        put_pix(self, i, 0, color)
        put_pix(self, i, self.can_h - 1, color)

    for i in range(self.can_h):
        put_pix(self, 0, i, color)
        put_pix(self, self.can_w - 1, i, color)


# Построчная закраска с затравкой
def fill_default(self):
    stack = []
    stack.append(self.seed)

    while len(stack) > 0:
        x, y = stack.pop()

        x_temp = x
        put_pix(self, x, y, self.fill_color)

        x += 1
        while get_pix(self, x, y) != self.bd_color:
            put_pix(self, x, y, self.fill_color)
            x += 1
        x_right = x - 1

        x = x_temp

        x -= 1
        while get_pix(self, x, y) != self.bd_color:
            put_pix(self, x, y, self.fill_color)
            x -= 1
        x_left = x + 1

        for i in range(1, -2, -2):
            x = x_left
            y += i
            while x <= x_right:
                flag = False

                while get_pix(self, x, y) != self.bd_color and get_pix(self, x, y) != self.fill_color and x < x_right:
                    if not flag:
                        flag = True
                    x += 1

                if flag:
                    if get_pix(self, x, y) != self.bd_color and get_pix(self, x, y) != self.fill_color and x == x_right:
                        stack.append((x, y))
                    else:
                        stack.append((x - 1, y))
                    flag = False

                x_enter = x
                while (get_pix(self, x, y) == self.bd_color or get_pix(self, x, y) == self.fill_color) and x < x_right:
                    x += 1

                if x == x_enter:
                    x += 1
            y -= i


# Построчная закраска с затравкой с задержкой
def fill_delay(self):
    stack = []
    stack.append(self.seed)

    while len(stack) > 0:
        QApplication.processEvents()

        x, y = stack.pop()

        x_temp = x
        put_pix(self, x, y, self.fill_color)

        x += 1
        while get_pix(self, x, y) != self.bd_color:
            put_pix(self, x, y, self.fill_color)
            x += 1
        x_right = x - 1

        x = x_temp

        x -= 1
        while get_pix(self, x, y) != self.bd_color:
            put_pix(self, x, y, self.fill_color)
            x -= 1
        x_left = x + 1

        self.repaint()

        for i in range(1, -2, -2):
            x = x_left
            y += i
            while x <= x_right:
                flag = False

                while get_pix(self, x, y) != self.bd_color and get_pix(self, x, y) != self.fill_color and x < x_right:
                    if not flag:
                        flag = True
                    x += 1

                if flag:
                    if get_pix(self, x, y) != self.bd_color and get_pix(self, x, y) != self.fill_color and x == x_right:
                        stack.append((x, y))
                    else:
                        stack.append((x - 1, y))
                    flag = False

                x_enter = x
                while (get_pix(self, x, y) == self.bd_color or get_pix(self, x, y) == self.fill_color) and x < x_right:
                    x += 1

                if x == x_enter:
                    x += 1
            y -= i
