from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys

from funcs import *
from cut import *


# Класс главного окна
class MyWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)

        # Загрузка интерфейса
        uic.loadUi("design.ui", self)

        # Переменные
        self.bg_color = QColor(Qt.white)
        self.line_color = QColor(Qt.black)
        self.cutter_color = QColor(Qt.red)
        self.cut_line_color = QColor(Qt.blue)

        self.ctrl_pressed = False
        self.lines = []
        self.cur_line = []
        self.follow_line = None

        self.cutter = None
        self.drawing_cutter = False
        self.follow_cutter = None

        # Добавляем полотно
        self.scene = QGraphicsScene(0, 0, 1920, 1080)
        self.mainview.setScene(self.scene)
        self.pen = QPen()
        self.mainview.ensureVisible(0, 0, 0, 0)
        self.mainview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mainview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Элементы ввода в интерфейсе
        self.inputs = [
            self.but_add_line,
            self.but_add_cutter,
            self.but_end_cutter,
            self.but_choose_cutter,
            self.but_cut,
            self.but_clear,
            self.inp_x1,
            self.inp_x2,
            self.inp_y1,
            self.inp_y2,
            self.inp_x_cutter,
            self.inp_y_cutter,
        ]

        # Настройка полей ввода
        reg_ex = QRegExp("[0-9]+")
        int_validator = QRegExpValidator(reg_ex, self)
        self.inp_x1.setValidator(int_validator)
        self.inp_x2.setValidator(int_validator)
        self.inp_y1.setValidator(int_validator)
        self.inp_y2.setValidator(int_validator)
        self.inp_x_cutter.setValidator(int_validator)
        self.inp_x_cutter.setValidator(int_validator)

        # Привязка кнопок
        self.but_add_line.clicked.connect(lambda: get_line(self))
        self.but_add_cutter.clicked.connect(lambda: get_cutter(self))
        self.but_end_cutter.clicked.connect(lambda: end_cutter(self))
        self.but_choose_cutter.clicked.connect(lambda: choose_cutter(self))
        self.but_cut.clicked.connect(lambda: cut(self))
        self.but_clear.clicked.connect(lambda: clear(self))

        # Остальные настройки
        self.mainview.setMouseTracking(True)
        self.mainview.viewport().installEventFilter(self)

    # Отслеживание передвижения мыши
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove and source is self.mainview.viewport():
            x = event.x()
            y = event.y()

            following_line(self, x, y)
            following_cutter(self, x, y)

        return QWidget.eventFilter(self, source, event)

    # Нажатие клавиши
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Control:
            self.ctrl_pressed = True

    # Отжатие клавиши
    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Control:
            self.ctrl_pressed = False

    # Нажатие кнопки мыши
    def mousePressEvent(self, event):
        but = event.button()
        x = event.x()
        y = event.y()
        borders = self.mainview.geometry().getCoords()
        if borders[0] <= x < borders[2] and borders[1] <= y < borders[3]:
            x -= borders[0]
            y -= borders[1]
        else:
            return

        if but == 1:
            line_on_screen(self, x, y)
            cutter_on_screen(self, x, y)

        if but == 2:
            end_cutter_on_screen(self)


def get_line(self):
    try:
        x1 = int(self.inp_x1.text())
        y1 = int(self.inp_y1.text())
        x2 = int(self.inp_x2.text())
        y2 = int(self.inp_y2.text())
    except ValueError:
        mes("Неверные данные отрезка")
        return -1

    add_line(self, x1, y1, x2, y2, self.line_color)


def get_cutter(self):
    pass


def end_cutter(self):
    pass


def choose_cutter(self):
    del_cutter(self)
    self.cutter = Cutter()
    self.drawing_cutter = True


def cut(self):
    if self.cutter and len(self.cutter.coords) > 2:
        if check_convex_polygon(self) == False:
            mes("Отсекатель невыпуклый")
            return -1




def clear(self):
    self.scene.clear()

    self.lines.clear()
    self.cur_line.clear()
    self.follow_line = None

    self.cutter = None
    self.follow_cutter = None
    self.drawing_cutter = False


if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
