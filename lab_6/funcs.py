from main import mes


# Returns edges from list of dots
def get_edges(dots_mas):
    edges = []

    for dots in dots_mas:
        for i in range(len(dots)):
            if i + 1 > len(dots) - 1:
                edges.append([dots[i], dots[0]])
            else:
                edges.append([dots[i], dots[i + 1]])

    return edges


# Adds edges on pixmap
def edges_to_pixmap(self):
    for edge in self.edges:
        x1 = edge[0][0]
        y1 = edge[0][1]
        x2 = edge[1][0]
        y2 = edge[1][1]

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_x == 0 and len_y == 0:
            self.pixmap[y1][x1] = self.bd_color
            continue

        n = max(len_x, len_y)

        dx = ((x2 > x1) - (x2 < x1)) * len_x / n
        dy = ((y2 > y1) - (y2 < y1)) * len_y / n

        for i in range(n + 1):
            self.pixmap[int(y1)][int(x1)] = self.bd_color
            x1 += dx
            y1 += dy


# Puts edges on image
def draw_edges(self):
    for edge in self.edges:
        x1 = edge[0][0]
        y1 = edge[0][1]
        x2 = edge[1][0]
        y2 = edge[1][1]

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_x == 0 and len_y == 0:
            self.img.put(self.bd_color, (x1, y1))
            continue

        n = max(len_x, len_y)

        dx = ((x2 > x1) - (x2 < x1)) * len_x / n
        dy = ((y2 > y1) - (y2 < y1)) * len_y / n

        for i in range(n + 1):
            self.img.put(self.bd_color, (int(x1), int(y1)))
            x1 += dx
            y1 += dy


def br_int_line(self, xy1, xy2):
    x1 = xy1[0]
    y1 = xy1[1]
    x2 = xy2[0]
    y2 = xy2[1]

    len_x = abs(int(x2) - int(x1))
    len_y = abs(int(y2) - int(y1))

    if len_x == 0 and len_y == 0:
        self.img.put(self.bd_color, (x1, y1))
        return -1

    n = max(len_x, len_y)

    dx = ((x2 > x1) - (x2 < x1)) * len_x / n
    dy = ((y2 > y1) - (y2 < y1)) * len_y / n

    for i in range(n + 1):
        self.img.put(self.bd_color, (int(x1), int(y1)))
        x1 += dx
        y1 += dy

    return 0


# Recolors pixmap and returns recolored pixels
def simple_seed_alg(self):
    try:
        seed_x = int(self.seed_x.get())
        seed_y = int(self.seed_y.get())
    except ValueError:
        mes("Неверно задана затравка!")
        return -1

    stack = []
    to_draw = []

    stack.append((seed_x, seed_y))

    while len(stack) != 0:
        cur_pix = stack.pop()
        x = cur_pix[0]
        y = cur_pix[1]

        min_x = 0
        max_x = len(self.pixmap[0]) - 1
        min_y = 0
        max_y = len(self.pixmap) - 1

        if self.pixmap[y][x] != self.fill_color:
            self.pixmap[y][x] = self.fill_color
            to_draw.append((x, y))

        if self.pixmap[y][x+1] != self.bd_color and self.pixmap[y][x+1] != self.fill_color and x + 1 < max_x:
            stack.append((x+1, y))
        if self.pixmap[y+1][x] != self.bd_color and self.pixmap[y+1][x] != self.fill_color and y + 1 < max_y:
            stack.append((x, y+1))
        if self.pixmap[y][x-1] != self.bd_color and self.pixmap[y][x-1] != self.fill_color and x - 1 > min_x:
            stack.append((x-1, y))
        if self.pixmap[y-1][x] != self.bd_color and self.pixmap[y-1][x] != self.fill_color and y - 1 > min_y:
            stack.append((x, y-1))

    return to_draw


# Converts pixmap to string
def pixmap_to_string(matrix):
    color_string = ""
    h = len(matrix)
    w = len(matrix[0])

    for i in range(h):
        color_string += '{'
        for j in range(w):
            color_string += matrix[i][j] + ' '
        color_string += '} '

    return color_string


# Changes pixmap to the size of canvas
def change_pixmap_size(self):
    dx = self.canvas.winfo_width() - len(self.pixmap[0])
    dy = self.canvas.winfo_height() - len(self.pixmap)

    for i in range(len(self.pixmap)):
        for j in range(abs(dx)):
            if dx > 0:
                self.pixmap[i].append(self.bg_color)
            else:
                self.pixmap[i].pop()

    for i in range(abs(dy)):
        if dy > 0:
            self.pixmap.append([self.bg_color for j in range(len(self.pixmap[0]))])
        else:
            self.pixmap.pop()


# Creates pixmap with bg color
def empty_pixmap(self):
    pixmap = [[self.bg_color for i in range(self.canvas.winfo_width())] for j in range(self.canvas.winfo_height())]

    return pixmap


# Puts pixmap on image
def draw_pixmap(self):
    color_string = pixmap_to_string(self.pixmap)

    for i in range(self.fig_n):
        self.canvas.delete("tag%s" % i)

    self.img.put(color_string, to=(0, 0, self.img.width(), self.img.height()))


# Puts pixels with delay using array of pixels
def draw_with_delay(self, to_draw):
    count = 10

    if len(to_draw) >= count:
        for i in range(count):
            pix = to_draw.pop(0)
            self.img.put(self.fill_color, pix)

        self.process = self.canvas.after(self.delay, lambda: draw_with_delay(self, to_draw))
    else:
        for i in range(len(to_draw)):
            pix = to_draw.pop(0)
            self.img.put(self.fill_color, pix)


# Print pixmap
def print_pixmap(pixmap):
    h = len(pixmap)
    w = len(pixmap[0])

    for i in range(h):
        for j in range(w):
            print(pixmap[i][j], end=" ")
        print()
