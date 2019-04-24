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


def add_line(self, x1, y1, x2, y2, color):
    self.pen.setColor(color)

    line = Line()

    line.x1 = x1
    line.y1 = y1
    line.x2 = x2
    line.y2 = y2
    line.scene_item = self.scene.addLine(x1, y1, x2, y2, self.pen)

    self.lines.append(line)


def add_cutter(self, x_l, y_u, x_r, y_d, color):
    self.pen.setColor(color)

    if x_l > x_r:
        x_l, x_r = x_r, x_l
    if y_u > y_d:
        y_u, y_d = y_d, y_u

    cutter = Cutter()

    cutter.x_left = x_l
    cutter.y_up = y_u
    cutter.x_right = x_r
    cutter.y_down = y_d
    cutter.scene_item = self.scene.addRect(x_l, y_u, x_r - x_l, y_d - y_u, self.pen)

    self.cutter = cutter


def del_cutter(self):
    if self.cutter:
        self.scene.removeItem(self.cutter.scene_item)
    self.cutter = None


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


def cutter_on_screen(self, x, y):
    if self.drawing_cutter:
        if len(self.cur_cutter) < 2:
            self.cur_cutter.append((x, y))

        if len(self.cur_cutter) == 2:
            c1, c2 = self.cur_cutter
            add_cutter(self, c1[0], c1[1], c2[0], c2[1], self.cutter_color)
            self.cur_cutter.clear()
            self.scene.removeItem(self.follow_cutter)
            self.drawing_cutter = False


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
    if len(self.cur_cutter) == 1:
        x_l, y_u = self.cur_cutter[0]
        x_r, y_d = x, y
        self.pen.setColor(self.cutter_color)

        if self.follow_cutter:
            self.scene.removeItem(self.follow_cutter)

        if x_l > x_r:
            x_l, x_r = x_r, x_l
        if y_u > y_d:
            y_u, y_d = y_d, y_u

        self.follow_cutter = self.scene.addRect(x_l, y_u, x_r - x_l, y_d - y_u, self.pen)
