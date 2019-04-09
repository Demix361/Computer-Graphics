

# Returns edges from list of dots
def get_edges(dots_mas):
    edges = []

    for dots in dots_mas:
        for i in range(len(dots)):
            if i + 1 > len(dots) - 1:
                edges.append([dots[i], dots[0]])
            else:
                edges.append([dots[i], dots[i + 1]])

    # faster:
    #edges = [[dots_mas[i][j], dots_mas[i][0]] if j + 1 > len(dots_mas[i]) - 1 else [dots_mas[i][j], dots_mas[i][j + 1]] for i in range(len(dots_mas)) for j in range(len(dots_mas[i]))]

    return edges


# Returns intersections from list of edges
def get_intersections(edges):
    intersections = []

    for i in range(len(edges)):
        x1 = edges[i][0][0]
        y1 = edges[i][0][1]
        x2 = edges[i][1][0]
        y2 = edges[i][1][1]

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_y != 0:
            dx = ((x2 > x1) - (x2 < x1)) * len_x / len_y
            dy = ((y2 > y1) - (y2 < y1))

            x1 += dx / 2
            y1 += dy / 2

            for j in range(len_y):
                intersections.append((x1, y1))
                x1 += dx
                y1 += dy

    return intersections


# Fills figure instantly
def fill_figure(self, inter):
    for i in range(0, len(inter), 2):
        draw_couple(self, inter[i], inter[i + 1])


# Fills figure with delay
def fill_delay(self, inter):
    cross1 = inter.pop()
    cross2 = inter.pop()

    draw_couple(self, cross1, cross2)


    if len(inter) > 0:
        self.process = self.canvas.after(self.delay, lambda:fill_delay(self, inter))
    else:
        draw_edges(self)


# Draws line between two dots
def draw_couple(self, dot1, dot2):
    x_beg = int(dot1[0] + 0.5)
    x_end = int(dot2[0] - 0.5) + 1
    y = int(dot1[1])

    self.canvas.create_line(x_beg, y, x_end, y, fill=self.fill_color)


# Draws edges
def draw_edges(self):
    for i in range(len(self.edges)):
        self.canvas.create_line(self.edges[i][0], self.edges[i][1], fill=self.bd_color)
