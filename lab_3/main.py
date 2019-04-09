import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from design import Ui_MainWindow
from copy import copy
from math import pi, sin, cos
from algorithms import *
from testing import time_test, step_test
import sys

class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Переменные
        self.lines = []

        # Добавляем canvas
        self.ui.canvas = Canvas(self)
        self.ui.canvas.setMinimumSize(QSize(600, 600))
        self.ui.canvas.setObjectName("canvas")
        self.ui.horizontalLayout.addWidget(self.ui.canvas)

        # Настраиваем поля ввода
        reg_ex = QRegExp("[0-9]+")
        int_validator = QRegExpValidator(reg_ex, self)
        self.ui.lineEdit_x1.setValidator(int_validator)
        self.ui.lineEdit_y1.setValidator(int_validator)
        self.ui.lineEdit_x2.setValidator(int_validator)
        self.ui.lineEdit_y2.setValidator(int_validator)
        self.ui.lineEdit_r.setValidator(int_validator)
        self.ui.lineEdit_a.setValidator(int_validator)
        self.ui.lineEdit_len.setValidator(int_validator)

        # Привязываем кнопки
        self.ui.pushButton_clr_line.setStyleSheet("background-color: rgb(0, 0, 0)")
        self.ui.pushButton_clr_back.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.ui.pushButton_clr_line.clicked.connect(self.get_color_line)
        self.ui.pushButton_clr_back.clicked.connect(self.get_color_bg)
        self.ui.pushButton_draw.clicked.connect(self.add_line)
        self.ui.pushButton_clear.clicked.connect(self.clear)
        self.ui.pushButton_time.clicked.connect(self.start_test_time)
        self.ui.pushButton_step.clicked.connect(self.start_test_step)


    def add_line(self):
        self.bg_change = True

        # Получаем данные
        if self.ui.tabWidget.currentIndex() == 0:
            try:
                x1 = float(self.ui.lineEdit_x1.text())
                y1 = float(self.ui.lineEdit_y1.text())
                x2 = float(self.ui.lineEdit_x2.text())
                y2 = float(self.ui.lineEdit_y2.text())
            except ValueError:
                print("Неверные данные!")
                return -1
        else:
            try:
                r = float(self.ui.lineEdit_r.text())
                angle = float(self.ui.lineEdit_a.text())
            except ValueError:
                print("Неверные данные!")
                return -2

        bg_color = list(map(int, self.ui.pushButton_clr_back.styleSheet()[22:-1].split(", ")))
        draw_bg = self.ui.checkBox_clr_back.checkState() // 2
        if draw_bg == 1:
            line_color = copy(bg_color)
        else:
            line_color = list(map(int, self.ui.pushButton_clr_line.styleSheet()[22:-1].split(", ")))
        alg = self.ui.comboBox_alg.currentIndex()

        # Добавляем линии в массив
        if self.ui.tabWidget.currentIndex() == 0:
            line = [x1, y1, x2, y2, line_color, bg_color, alg]
            self.lines.append(line)
        else:
            cur = 0
            end = pi * 2
            xc = 300
            yc = 300

            while cur < end:
                x = xc + cos(cur) * r
                y = yc + sin(cur) * r

                line = [xc, yc, round(x), round(y), line_color, bg_color, alg]
                self.lines.append(line)
                cur += angle * pi / 180


    def clear(self):
        self.lines = []

    def get_color_line(self):
        tmp = QColorDialog.getColor()

        if tmp.isValid():
            tmp = tmp.getRgb()
            self.ui.pushButton_clr_line.setStyleSheet("background-color: rgb(%d, %d, %d)" % (tmp[0], tmp[1], tmp[2]))

    def get_color_bg(self):
        tmp = QColorDialog.getColor()

        if tmp.isValid():
            tmp = tmp.getRgb()
            self.ui.pushButton_clr_back.setStyleSheet("background-color: rgb(%d, %d, %d)" % (tmp[0], tmp[1], tmp[2]))
            for line in self.lines:
                line[5] = tmp

    def start_test_time(self):
        try:
            length = float(self.ui.lineEdit_len.text())
        except ValueError:
            print("Неверные данные!")
            return -1
        time_test(length)

    def start_test_step(self):
        try:
            length = float(self.ui.lineEdit_len.text())
        except ValueError:
            print("Неверные данные!")
            return -1

        alg = self.ui.comboBox_alg.currentIndex()
        step_test(length, alg)


class Canvas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.show()


    def paintEvent(self, event):
        painter = QPainter()

        painter.begin(self)

        bg = list(map(int, self.parent.ui.pushButton_clr_back.styleSheet()[22:-1].split(", ")))

        painter.setPen(QColor(bg[0], bg[1], bg[2]))
        painter.setBrush(QColor(bg[0], bg[1], bg[2]))
        painter.drawRect(0, 0, self.width(), self.height())

        drawline(painter, self.parent.lines)

        painter.end()
        self.update()

def drawline(painter, lines):
    if lines != []:
        for line in lines:
            painter.setPen(QColor(line[4][0], line[4][1], line[4][2]))
            
            if line[6] == 0:
                drawline_dda(painter,line[0],line[1],line[2],line[3])
            if line[6] == 1:
                drawline_br_int(painter,line[0],line[1],line[2],line[3])
            if line[6] == 2:
                drawline_br_float(painter,line[0],line[1],line[2],line[3])
            if line[6] == 3:
                drawline_br_smooth(painter, line[0], line[1], line[2], line[3], line[4], line[5])
            if line[6] == 4:
                drawline_wu(painter,line[0],line[1],line[2],line[3],line[4], line[5])
            if line[6] == 5:
                drawline_std(painter,line[0],line[1],line[2],line[3])

if __name__ == '__main__':
    app = QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())
