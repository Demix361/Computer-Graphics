from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import os

import pyqtgraph.opengl as gl
from pyqtgraph import mkColor, glColor
import numpy as np
from d_s import diamond_square
from time import time



class MyWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)

        # Загрузка интерфейса
        uic.loadUi("design.ui", self)

        self.w = gl.GLViewWidget(self.centralwidget)
        self.horizontalLayout.addWidget(self.w)
        self.w.show()

        # Переменные
        self.landscape = None
        self.polygon_color = QColor("#0ea01f")

        # Настройка GL виджета
        self.w.setCameraPosition(distance=30, elevation=8)
        grid = gl.GLGridItem()
        grid.scale(2, 2, 2)
        #self.w.addItem(grid)

        # Привязка кнопок
        self.pushButton.clicked.connect(lambda: build_terrain(self))
        self.but_color.clicked.connect(lambda: get_color(self))

        # Другие настройки
        self.label_color.setStyleSheet("background-color: rgb(%d, %d, %d)" % self.polygon_color.getRgb()[:3])



def build_terrain(self):
    try:
        p1 = float(self.lineEdit_2.text())
        p2 = float(self.lineEdit_3.text())
        p3 = float(self.lineEdit_4.text())
        p4 = float(self.lineEdit_5.text())
        rand_low = float(self.lineEdit_6.text())
        rand_high = float(self.lineEdit_7.text())
        size = int(self.lineEdit.text())
        shader = str(self.comboBox.currentText())
        draw_edges = self.checkBox.isChecked()
        smooth = self.checkBox_2.isChecked()
    except ValueError:
        return -1

    nstep = 1
    ypoints = range(-(size // 2), size // 2 + 1, nstep)
    xpoints = range(-(size // 2), size // 2 + 1, nstep)
    nfaces = len(ypoints)
    verts = np.array([
        [x, y, 0] for n, x in enumerate(xpoints) for m, y in enumerate(ypoints)
    ], dtype=np.float32)

    verts_temp = [[0 for j in range(size)] for i in range(size)]
    diamond_square(verts_temp, p1, p2, p3, p4, [rand_low, rand_high])
    for i in range(len(verts_temp)):
        for j in range(len(verts_temp)):
            verts[i * len(verts_temp) + j][2] = verts_temp[i][j]

    beg = time()
    faces = []
    #colors = [glColor("#0ea01f") for i in range((nfaces - 1)**2 * 2)]
    end = time()
    print(end - beg)


    for m in range(nfaces - 1):
        yoff = m * nfaces
        for n in range(nfaces - 1):
            faces.append([n + yoff, yoff + n + nfaces, yoff + n + nfaces + 1])
            faces.append([n + yoff, yoff + n + 1, yoff + n + nfaces + 1])

    faces = np.array(faces)
    #colors = np.array(colors)



    m1 = gl.GLMeshItem(
        vertexes=verts,
        faces=faces, #faceColors=colors,
        color=self.polygon_color,
        glOptions='opaque', shader=shader,
        smooth=smooth, drawEdges=draw_edges
    )

    if self.landscape:
        self.w.removeItem(self.landscape)

    self.landscape = m1
    self.w.addItem(m1)


def mes(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle("Внимание")
    msg.setText(text)

    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()


def get_color(self):
    color = QColorDialog.getColor()

    if color.isValid():
        self.label_color.setStyleSheet("background-color: rgb(%d, %d, %d)" % color.getRgb()[:3])
        self.polygon_color = color





def convert():
    path_pyuic5 = "C:\\Users\\ti-am\\AppData\\Local\\Programs\\Python\\Python37\\Scripts\\pyuic5.exe"
    os.system("%s design.ui -o design.py" % path_pyuic5)


def rgba(hex_str):
    hex_str = hex_str.lstrip('#')
    rgb = list(int(hex_str[i:i + 2], 16) / 255 for i in (0, 2, 4))

    rgb.append(1.)

    return rgb




if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
