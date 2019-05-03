from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys

from funcs import *
from simple_cut import easy_cut


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
        self.can_w = 600
        self.can_h = 600

        self.ctrl_pressed = False
        self.lines = []
        self.cur_line = []
        self.follow_line = None

        self.cutter = None
        self.drawing_cutter = False
        self.cur_cutter = []
        self.follow_cutter = None

        # Добавляем полотно
        self.scene = QGraphicsScene(0, 0, self.can_w, self.can_h)
        self.mainview.setScene(self.scene)
        self.image = QImage(self.can_w, self.can_h, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.pixmap = QPixmap(self.can_w, self.can_h)

        # Элементы ввода в интерфейсе
        self.inputs = [
            self.but_add_line,
            self.but_add_cutter,
            self.but_choose_cutter,
            self.but_cut,
            self.but_clear,
            self.inp_x1,
            self.inp_x2,
            self.inp_y1,
            self.inp_y2,
            self.inp_x_left,
            self.inp_x_right,
            self.inp_y_up,
            self.inp_y_down
        ]

        # Настройка полей ввода
        reg_ex = QRegExp("[0-9]+")
        int_validator = QRegExpValidator(reg_ex, self)
        self.inp_x1.setValidator(int_validator)
        self.inp_x2.setValidator(int_validator)
        self.inp_y1.setValidator(int_validator)
        self.inp_y2.setValidator(int_validator)
        self.inp_x_left.setValidator(int_validator)
        self.inp_x_right.setValidator(int_validator)
        self.inp_y_up.setValidator(int_validator)
        self.inp_y_down.setValidator(int_validator)

        # Привязка кнопок
        self.but_add_line.clicked.connect(lambda: get_line(self))
        self.but_add_cutter.clicked.connect(lambda: get_cutter(self))
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
    try:
        x_left = int(self.inp_x_left.text())
        y_up = int(self.inp_y_up.text())
        x_right = int(self.inp_x_right.text())
        y_down = int(self.inp_y_down.text())
    except ValueError:
        mes("Неверные данные отрезка")
        return -1

    del_cutter(self)
    add_cutter(self, x_left, y_up, x_right, y_down, self.cutter_color)


def choose_cutter(self):
    del_cutter(self)
    self.drawing_cutter = True


def cut(self):
    if self.cutter:
        for i in range(len(self.lines)):
            xl = self.cutter.x_left
            xr = self.cutter.x_right
            yd = self.cutter.y_down
            yu = self.cutter.y_up
            p1 = [self.lines[i].x1, self.lines[i].y1]
            p2 = [self.lines[i].x2, self.lines[i].y2]
            yu, yd = yd, yu

            visible, p1, p2 = easy_cut(xl, xr, yd, yu, p1, p2)
            if visible:
                draw_line(self, p1, p2, self.cut_line_color)


def clear(self):
    self.scene.clear()

    self.lines.clear()
    self.cur_line.clear()
    self.follow_line = None

    self.cutter = None
    self.cur_cutter.clear()
    self.follow_cutter = None
    self.drawing_cutter = False


if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
