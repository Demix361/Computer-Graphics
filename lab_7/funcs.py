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
