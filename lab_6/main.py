from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
from random import randint

from funcs import create_line


class MyWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)

        # Загрузка интерфейса
        uic.loadUi("design.ui", self)

        # Переменные
        self.bg_color = QColor(Qt.white)
        self.bd_color = QColor(Qt.black)
        self.fill_color = QColor(Qt.red)
        self.can_w = 600
        self.can_h = 600
        self.seed = None
        self.choosing_seed = False
        self.ctrl_pressed = False
        self.first_dot = None
        self.cur_figure = []
        self.follow_line = None

        # Добавляем холст
        self.scene = QGraphicsScene(0, 0, self.can_w, self.can_h)
        self.mainview.setScene(self.scene)
        self.image = QImage(self.can_w, self.can_h, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.pen.setColor(self.bd_color)
        self.pixmap = QPixmap(self.can_w, self.can_h)

        # Настройка полей ввода
        reg_ex = QRegExp("[0-9]+")
        int_validator = QRegExpValidator(reg_ex, self)
        self.lineEdit_x.setValidator(int_validator)
        self.lineEdit_y.setValidator(int_validator)
        self.lineEdit_seed_x.setValidator(int_validator)
        self.lineEdit_seed_y.setValidator(int_validator)

        # Привязка кнопок
        self.pushButton_bd_clr.clicked.connect(lambda: get_color_bd(self))
        self.pushButton_fill_clr.clicked.connect(lambda: get_color_fill(self))
        self.pushButton_seed.clicked.connect(lambda: get_seed(self))
        self.pushButton_add.clicked.connect(lambda: press_add_dot(self))
        self.pushButton_end.clicked.connect(lambda: end(self))
        self.pushButton_clear.clicked.connect(lambda: clear(self))

        # Остальные настройки
        self.mainview.setMouseTracking(True)
        self.mainview.viewport().installEventFilter(self)
        self.label_bd.setStyleSheet("background-color: rgb(%d, %d, %d)" % self.bd_color.getRgb()[:3])
        self.label_fill.setStyleSheet("background-color: rgb(%d, %d, %d)" % self.fill_color.getRgb()[:3])

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove and source is self.mainview.viewport():
            x = event.x()
            y = event.y()

            if len(self.cur_figure) > 0:
                prev = self.cur_figure[-1]
                if self.ctrl_pressed:
                    if self.follow_line:
                        self.scene.removeItem(self.follow_line)

                    dx = x - prev[0]
                    dy = y - prev[1]

                    if abs(dy) >= abs(dx):
                        cur = (prev[0], y)
                    else:
                        cur = (x, prev[1])

                    self.follow_line = self.scene.addLine(prev[0], prev[1], cur[0], cur[1], self.pen)
                else:
                    if self.follow_line:
                        self.scene.removeItem(self.follow_line)
                    self.follow_line = self.scene.addLine(prev[0], prev[1], x, y, self.pen)

        return QWidget.eventFilter(self, source, event)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Control:
            self.ctrl_pressed = True

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Control:
            self.ctrl_pressed = False

    def mousePressEvent(self, event):
        but = event.button()

        if but == 1 or but == 2:
            x = event.x()
            y = event.y()
            borders = self.mainview.geometry().getCoords()

            if borders[0] <= x < borders[2] and borders[1] <= y < borders[3]:
                x -= borders[0]
                y -= borders[1]

                if but == 1:
                    if self.choosing_seed:
                        self.seed = (x, y)
                        QApplication.restoreOverrideCursor()
                        self.choosing_seed = False
                        self.lineEdit_seed_x.setText(str(x))
                        self.lineEdit_seed_y.setText(str(y))
                    elif self.ctrl_pressed == 0 or len(self.cur_figure) == 0:
                        add_dot(self, x, y)
                    else:
                        prev = self.cur_figure[-1]

                        dx = x - prev[0]
                        dy = y - prev[1]

                        if abs(dy) >= abs(dx):
                            add_dot(self, prev[0], y)
                        else:
                            add_dot(self, x, prev[1])

                elif but == 2:
                    end(self)


def press_add_dot(self):
    try:
        x = int(self.lineEdit_x.text())
        y = int(self.lineEdit_y.text())
    except ValueError:
        mes("Неверные координаты точки")
        return -1

    # ПРОВЕРКА НА ВХОЖДЕНИЕ В ОБЛАСТЬ
    add_dot(self, x, y)


def add_dot(self, x, y):
    self.cur_figure.append((x, y))

    if len(self.cur_figure) > 1:
        create_line(self, self.cur_figure[-2], self.cur_figure[-1])

    self.pixmap.convertFromImage(self.image)
    self.scene.addPixmap(self.pixmap)
    self.scene.removeItem(self.follow_line)


def end(self):
    if len(self.cur_figure) > 2:
        create_line(self, self.cur_figure[-1], self.cur_figure[0])

        self.cur_figure.clear()

        self.pixmap.convertFromImage(self.image)
        self.scene.addPixmap(self.pixmap)
        self.scene.removeItem(self.follow_line)


def get_color_bd(self):
    color = QColorDialog.getColor()

    if color.isValid():
        self.label_bd.setStyleSheet("background-color: rgb(%d, %d, %d)" % color.getRgb()[:3])
        self.bd_color = color
        self.pen.setColor(self.bd_color)


def get_color_fill(self):
    color = QColorDialog.getColor()

    if color.isValid():
        self.label_fill.setStyleSheet("background-color: rgb(%d, %d, %d)" % color.getRgb()[:3])
        self.fill_color = color


def get_seed(self):
    QApplication.setOverrideCursor(Qt.CrossCursor)
    self.choosing_seed = True


def clear(self):
    self.scene.clear()
    self.image.fill(self.bg_color)


def mes(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle("Внимание")
    msg.setText(text)

    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()


if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())