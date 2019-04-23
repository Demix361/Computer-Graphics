from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys

from funcs import create_line, fill_default, fill_delay, put_borders, create_circle


# Класс главного окна
class MyWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)

        # Загрузка интерфейса
        uic.loadUi("design.ui", self)

        # Переменные
        self.bg_color = QColor(Qt.white)
        self.bd_color = QColor(Qt.black)
        self.fill_color = QColor("#ff8263")
        self.can_w = 600
        self.can_h = 600
        self.seed = None
        self.choosing_seed = False
        self.ctrl_pressed = False
        self.first_dot = None
        self.cur_figure = []
        self.follow_line = None
        self.drawing_circle = False
        self.circle = None
        self.follow_circle = None

        # Добавляем полотно
        self.scene = QGraphicsScene(0, 0, self.can_w, self.can_h)
        self.mainview.setScene(self.scene)
        self.image = QImage(self.can_w, self.can_h, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.pen.setColor(self.bd_color)
        self.pixmap = QPixmap(self.can_w, self.can_h)

        # Элементы ввода в интерфейсе
        self.inputs = [
            self.pushButton_bd_clr,
            self.pushButton_fill_clr,
            self.pushButton_seed,
            self.pushButton_add,
            self.pushButton_end,
            self.pushButton_clear,
            self.pushButton_fill,
            self.lineEdit_x,
            self.lineEdit_y,
            self.lineEdit_seed_x,
            self.lineEdit_seed_y,
            self.checkBox
        ]

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
        self.pushButton_fill.clicked.connect(lambda: fill(self))
        self.pushButton_circle.clicked.connect(lambda: add_circle(self))

        # Остальные настройки
        self.mainview.setMouseTracking(True)
        self.mainview.viewport().installEventFilter(self)
        self.label_bd.setStyleSheet("background-color: rgb(%d, %d, %d)" % self.bd_color.getRgb()[:3])
        self.label_fill.setStyleSheet("background-color: rgb(%d, %d, %d)" % self.fill_color.getRgb()[:3])

    # Отслеживание передвижения мыши
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

            if self.drawing_circle:
                if self.circle:
                    xc, yc = self.circle

                    if self.follow_circle:
                        self.scene.removeItem(self.follow_circle)
                    r = (abs(x - xc)**2 + abs(y - yc)**2)**0.5
                    self.follow_circle = self.scene.addEllipse(xc - r, yc - r, 2 * r, 2 * r, self.pen)

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

        if but == 1 or but == 2:
            x = event.x()
            y = event.y()
            borders = self.mainview.geometry().getCoords()

            if borders[0] <= x < borders[2] and borders[1] <= y < borders[3]:
                x -= borders[0]
                y -= borders[1]

                if but == 1:
                    # Затравка
                    if self.choosing_seed:
                        self.lineEdit_seed_x.setText(str(x))
                        self.lineEdit_seed_y.setText(str(y))

                        QApplication.restoreOverrideCursor()
                        self.choosing_seed = False
                        enable_buttons(self.inputs)

                    # Окружность
                    elif self.drawing_circle:
                        if not self.circle:
                            self.circle = (x, y)
                        else:
                            r = round((abs(self.circle[0] - x)**2 + abs(self.circle[1] - y)**2)**0.5)
                            create_circle(self, self.circle, r)

                            self.drawing_circle = False
                            self.circle = None

                            add_pixmap(self)
                            self.scene.removeItem(self.follow_circle)

                            enable_buttons(self.inputs)

                    # Обычный отрезок
                    elif self.ctrl_pressed == 0 or len(self.cur_figure) == 0:
                        add_dot(self, x, y)

                    # Отрезок под прямым углом
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

    # pixmap на сцену (для закраски с задержкой)
    def paintEvent(self, event):
        self.scene.clear()
        add_pixmap(self)


# Закрашивает область с задержкой или без
def fill(self):
    try:
        x = int(self.lineEdit_seed_x.text())
        y = int(self.lineEdit_seed_y.text())
    except ValueError:
        mes("Неверные координаты затравки")
        return -1

    if not 0 < x < self.can_w - 1 or not 0 < y < self.can_h - 1:
        mes("Неверные координаты затравки")
        return -2

    self.seed = (x, y)

    put_borders(self, self.bd_color)

    if self.checkBox.checkState() == 0:
        fill_default(self)
    else:
        fill_delay(self)

    put_borders(self, self.bg_color)
    add_pixmap(self)


# Получает данные и вызывает add_dot
def press_add_dot(self):
    try:
        x = int(self.lineEdit_x.text())
        y = int(self.lineEdit_y.text())
    except ValueError:
        mes("Неверные координаты точки")
        return -1

    if x <= self.can_w and y <= self.can_h:
        add_dot(self, x, y)


# Добавляет точку в список и рисует отрезок
def add_dot(self, x, y):
    if 0 <= x < self.can_w and 0 <= y < self.can_h:
        self.cur_figure.append((x, y))

        if len(self.cur_figure) > 1:
            create_line(self, self.cur_figure[-2], self.cur_figure[-1])

        add_pixmap(self)
        self.scene.removeItem(self.follow_line)


# Соединяет последнюю точку с первой
def end(self):
    if len(self.cur_figure) > 2:
        create_line(self, self.cur_figure[-1], self.cur_figure[0])

        self.cur_figure.clear()

        add_pixmap(self)
        self.scene.removeItem(self.follow_line)


# Устанавливает переменную рисования окружности
def add_circle(self):
    self.drawing_circle = True
    disable_buttons(self.inputs)


# Создает pixmap из image, привязывает pixmap к сцене
def add_pixmap(self):
    self.pixmap.convertFromImage(self.image)
    self.scene.addPixmap(self.pixmap)


# Цвет границы
def get_color_bd(self):
    color = QColorDialog.getColor()

    if color.isValid():
        self.label_bd.setStyleSheet("background-color: rgb(%d, %d, %d)" % color.getRgb()[:3])
        self.bd_color = color
        self.pen.setColor(self.bd_color)


# Цвет закраски
def get_color_fill(self):
    color = QColorDialog.getColor()

    if color.isValid():
        self.label_fill.setStyleSheet("background-color: rgb(%d, %d, %d)" % color.getRgb()[:3])
        self.fill_color = color


# Устанавливает переменную получения затравки
def get_seed(self):
    disable_buttons(self.inputs)
    QApplication.setOverrideCursor(Qt.CrossCursor)
    self.choosing_seed = True


# Очищает полотно
def clear(self):
    self.scene.clear()
    self.image.fill(self.bg_color)


# Выводит окно с предупреждением
def mes(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle("Внимание")
    msg.setText(text)

    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()


# Отключает кнопки, переданные в списке
def disable_buttons(buttons):
    for b in buttons:
        b.setEnabled(False)


# Включает кнопки, переданные в списке
def enable_buttons(buttons):
    for b in buttons:
        b.setEnabled(True)


# Возвращает список без заданного элемента
def without(array, element):
    new_array = array.copy()
    new_array.remove(element)

    return new_array


if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
