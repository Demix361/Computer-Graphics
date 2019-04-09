from math import pi, sin, cos
from time import time
from algorithms_test import *
import numpy as np
import matplotlib.pyplot as plt


def time_test(line_len):
    lines = []

    cur = 0
    end = 2 * pi
    xc = 0
    yc = 0
    angle = 2

    while cur < end:
        x = xc + cos(cur) * line_len
        y = yc + sin(cur) * line_len

        line = [xc, yc, round(x), round(y), [0, 0, 0], [255, 255, 255]]
        lines.append(line)
        cur += angle * pi / 180

    n = len(lines)

    beg = time()
    for line in lines:
        test_dda(line[0], line[1], line[2], line[3])
    end = time()
    time_dda = (end - beg) / n

    beg = time()
    for line in lines:
        test_br_float(line[0], line[1], line[2], line[3])
    end = time()
    time_br_float = (end - beg) / n

    beg = time()
    for line in lines:
        test_br_int(line[0], line[1], line[2], line[3])
    end = time()
    time_br_int = (end - beg) / n

    beg = time()
    for line in lines:
        test_br_smooth(line[0], line[1], line[2], line[3], line[4], line[5])
    end = time()
    time_br_smooth = (end - beg) / n

    beg = time()
    for line in lines:
        test_wu(line[0], line[1], line[2], line[3], line[4], line[5])
    end = time()
    time_wu = (end - beg) / n


    print("dda:", time_dda)
    print("br_float", time_br_float)
    print("br_int", time_br_int)
    print("br_smooth", time_br_smooth)
    print("wu", time_wu)
    print()

    data_names = ["ЦДА", "Брезенхем", "Брезенхем\nцелочисленный",
                  "Брезенхем без\nступенчатости", "Алгоритм Ву"]
    data_values = [time_dda, time_br_float, time_br_int, time_br_smooth, time_wu]

    ind = np.arange(5)
    width = 0.35

    plt.bar(ind, data_values, width)
    plt.ylabel("Время, с.")
    plt.xticks(ind, data_names)
    plt.title("Время постороения отрезка длины " + str(int(line_len)) + " пикс.")
    plt.show()

def step_test(line_len, alg):
    lines = []
    steps = []

    cur = 0
    end = pi / 4
    xc = 0
    yc = 0
    angle = 1

    while cur < end + 0.01:
        x = xc + cos(cur) * line_len
        y = yc + sin(cur) * line_len

        line = [xc, yc, round(x), round(y), [0, 0, 0], [255, 255, 255], alg]
        lines.append(line)
        cur += angle * pi / 180

    n = len(lines)
    print("n ", n)

    for line in lines:
        if line[6] == 0:
            steps.append(step_dda(line[0], line[1], line[2], line[3]))
            #print("x1: ", line[0], "\t\ty1: ", line[1], "\nx2: ", line[2], "\t\ty2: ", line[3])
        if line[6] == 1:
            steps.append(step_br_int(line[0], line[1], line[2], line[3]))
        if line[6] == 2:
            steps.append(step_br_float(line[0], line[1], line[2], line[3]))
        if line[6] == 3:
            steps.append(step_br_smooth(line[0], line[1], line[2], line[3], line[4], line[5]))
        if line[6] == 4:
            steps.append(step_wu(line[0], line[1], line[2], line[3], line[4], line[5]))

    alg_names = ["ЦДА", "Брезенхем\nцелочисленный", "Брезенхем",
                  "Брезенхем без\nступенчатости", "Алгоритм Ву"]
    x = [i for i in range(n)]
    plt.plot(x, steps)
    plt.ylabel("Длина макс. ступеньки")
    plt.xlabel("Угол наклона")
    plt.title(alg_names[lines[0][6]] + "\nДлина отрезка " + str(int(line_len)) + " пикс.")
    plt.show()
    plt.close()
