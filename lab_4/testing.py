from time import time
from algorithms_test import *


# Draws graphs of time efficiency of different algs
def time_test(n):
    circles = []

    time_canon = []
    time_param = []
    time_br = []
    time_mid = []
    r_mas = []

    for r in range(0, n, 100):
        circles.append([500, 500, r])
        r_mas.append(r)


    for c in circles:
        beg = time()
        test_circle_canon(c[0], c[1], c[2])
        end = time()
        time_canon.append(end - beg)

    for c in circles:
        beg = time()
        test_circle_param(c[0], c[1], c[2])
        end = time()
        time_param.append(end - beg)

    for c in circles:
        beg = time()
        test_circle_br(c[0], c[1], c[2])
        end = time()
        time_br.append(end - beg)

    for c in circles:
        beg = time()
        test_circle_mid(c[0], c[1], c[2])
        end = time()
        time_mid.append(end - beg)

    return time_canon, time_param, time_br, time_mid, r_mas
