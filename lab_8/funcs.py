from PyQt5.QtWidgets import QMessageBox
from structs import *


# Выводит окно с предупреждением
def mes(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle("Внимание")
    msg.setText(text)

    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()


# Рисует отрезки
def add_line(self, x1, y1, x2, y2, color):
    self.pen.setColor(color)

    line = Line()

    line.x1 = x1
    line.y1 = y1
    line.x2 = x2
    line.y2 = y2
    line.scene_item = self.scene.addLine(x1, y1, x2, y2, self.pen)

    self.lines.append(line)


def redraw_cutter(self):
    if self.cutter:
        n = len(self.cutter.coords)

        for i in self.cutter.scene_items:
            self.scene.removeItem(i)
        self.cutter.scene_items.clear()

        self.pen.setColor(self.cutter_color)
        for i in range(n):
            p1 = self.cutter.coords[i - 1]
            p2 = self.cutter.coords[i]

            self.cutter.scene_items.append(self.scene.addLine(p1[0], p1[1], p2[0], p2[1], self.pen))


# OK
def del_cutter(self):
    if self.cutter:
        for c in self.cutter.scene_items:
            self.scene.removeItem(c)
        self.cutter = None


# OK Рисует отрезки
def line_on_screen(self, x, y):
    if not self.drawing_cutter:
        if self.ctrl_pressed == 0 or len(self.cur_line) == 0:
            self.cur_line.append((x, y))

        else:
            prev = self.cur_line[0]

            dx = x - prev[0]
            dy = y - prev[1]

            if abs(dy) >= abs(dx):
                self.cur_line.append((prev[0], y))
            else:
                self.cur_line.append((x, prev[1]))

        if len(self.cur_line) == 2:
            c1, c2 = self.cur_line
            add_line(self, c1[0], c1[1], c2[0], c2[1], self.line_color)
            self.cur_line.clear()
            self.scene.removeItem(self.follow_line)
            redraw_cutter(self)


def cutter_on_screen(self, x, y):
    if self.drawing_cutter:
        self.pen.setColor(self.cutter_color)

        c = self.cutter.coords

        if self.ctrl_pressed == 0 or len(c) == 0:
            c.append((x, y))

        else:
            prev = c[-1]

            dx = x - prev[0]
            dy = y - prev[1]

            if abs(dy) >= abs(dx):
                c.append((prev[0], y))
            else:
                c.append((x, prev[1]))

        if len(c) > 1:
            self.cutter.scene_items.append(self.scene.addLine(c[-1][0], c[-1][1], c[-2][0], c[-2][1], self.pen))


def end_cutter_on_screen(self):
    if self.drawing_cutter:
        self.pen.setColor(self.cutter_color)

        if len(self.cutter.coords) > 2:
            c = self.cutter.coords
            self.cutter.scene_items.append(self.scene.addLine(c[-1][0], c[-1][1], c[0][0], c[0][1], self.pen))

            self.drawing_cutter = False
            self.scene.removeItem(self.follow_cutter)



# OK
def following_line(self, x, y):
    if len(self.cur_line) == 1:
        prev = self.cur_line[0]
        self.pen.setColor(self.line_color)

        if self.follow_line:
            self.scene.removeItem(self.follow_line)

        if self.ctrl_pressed:
            dx = x - prev[0]
            dy = y - prev[1]

            if abs(dy) >= abs(dx):
                cur = (prev[0], y)
            else:
                cur = (x, prev[1])

            self.follow_line = self.scene.addLine(prev[0], prev[1], cur[0], cur[1], self.pen)
        else:
            self.follow_line = self.scene.addLine(prev[0], prev[1], x, y, self.pen)


def following_cutter(self, x, y):
    if self.drawing_cutter and len(self.cutter.coords) > 0:
        prev = self.cutter.coords[-1]
        self.pen.setColor(self.cutter_color)

        if self.follow_cutter:
            self.scene.removeItem(self.follow_cutter)

        if self.ctrl_pressed:
            dx = x - prev[0]
            dy = y - prev[1]

            if abs(dy) >= abs(dx):
                cur = (prev[0], y)
            else:
                cur = (x, prev[1])

            self.follow_cutter = self.scene.addLine(prev[0], prev[1], cur[0], cur[1], self.pen)
        else:
            self.follow_cutter = self.scene.addLine(prev[0], prev[1], x, y, self.pen)


# OK
def draw_line(self, dot1, dot2, color):
    self.pen.setColor(color)
    self.scene.addLine(dot1[0], dot1[1], dot2[0], dot2[1], self.pen)


def highlight(self, p1, p2):
    self.pen.setColor(self.cut_line_color)
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])

    for i in range(3):
        if dx > dy:
            line = self.scene.addLine(p1[0], p1[1] - 1 + i, p2[0], p2[1] - 1 + i, self.pen)
        else:
            line = self.scene.addLine(p1[0] - 1 + i, p1[1], p2[0] - 1 + i, p2[1], self.pen)

        self.highlighted_lines.append(line)


def remove_highlight(self):
    for i in self.highlighted_lines:
        self.scene.removeItem(i)
    self.highlighted_lines.clear()


