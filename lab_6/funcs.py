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


# Добавляет границы вокруг карты пикселей
def borders_to_pixmap(self):
    for i in range(len(self.pixmap[0])):
        self.pixmap[0][i] = self.bd_color
        self.pixmap[-1][i] = self.bd_color
    for i in range(len(self.pixmap)):
        self.pixmap[i][0] = self.bd_color
        self.pixmap[i][-1] = self.bd_color


# Добавляет грани фигур на карту пикселей
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


# Простой алгоритм с затравкой
def simple_seed_alg(self):
    try:
        seed_x = int(self.seed_x.get())
        seed_y = int(self.seed_y.get())
    except ValueError:
        mes("Неверно задана затравка!")
        return -1

    stack = []

    stack.append((seed_x, seed_y))

    while len(stack) != 0:
        cur_pix = stack.pop()
        x = cur_pix[0]
        y = cur_pix[1]

        min_x = 0
        max_x = len(self.pixmap[0]) - 1
        min_y = 0
        max_y = len(self.pixmap) - 1
        if x - 1 < 0 or x + 1 >= len(self.pixmap[0]) or y - 1 < 0 or y + 1 >= len(self.pixmap):
            print("error (%s, %s)" % (x, y))

        self.pixmap[y][x] = self.fill_color

        if self.pixmap[y][x+1] != self.bd_color and self.pixmap[y][x+1] != self.fill_color and x + 1 < max_x:
            stack.append((x+1, y))
        if self.pixmap[y+1][x] != self.bd_color and self.pixmap[y+1][x] != self.fill_color and y + 1 < max_y:
            stack.append((x, y+1))
        if self.pixmap[y][x-1] != self.bd_color and self.pixmap[y][x-1] != self.fill_color and x - 1 > min_x:
            stack.append((x-1, y))
        if self.pixmap[y-1][x] != self.bd_color and self.pixmap[y-1][x] != self.fill_color and y - 1 > min_y:
            stack.append((x, y-1))


# Конвертирует карту пикселей в строчный формат
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



def empty_pixmap(self):
    pixmap = [[self.bg_color for i in range(self.canvas.winfo_width())] for j in range(self.canvas.winfo_height())]

    return pixmap

def create_pixmap(self):
    pixmap = []
    h = self.canvas.winfo_height()
    w = self.canvas.winfo_width()

    for i in range(h):
        pixmap.append([])
        for j in range(w):
            if j == 0 or j == w - 1 or i == 0 or i == h - 1:
                pixmap[i].append("#000000")
            else:
                pixmap[i].append("#ffffff")

    return pixmap

def draw_pixmap(self):
    color_string = pixmap_to_string(self.pixmap)

    self.canvas.delete("tag0")
    self.canvas.delete("tag1")

    self.img.put(color_string, to=(0, 0, self.img.width(), self.img.height()))


# Печать карты пикселей
def print_pixmap(pixmap):
    h = len(pixmap)
    w = len(pixmap[0])

    for i in range(h):
        for j in range(w):
            print(pixmap[i][j], end=" ")
        print()

