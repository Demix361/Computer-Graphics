from math import log
from random import uniform


def mid(*args):
    s = 0
    for i in range(len(args)):
        s += args[i]
    s /= len(args)

    return s


def square_step(arr, i, j, d, rand):
    k = d // 2
    arr[i + k][j + k] = mid(arr[i][j], arr[i + d][j], arr[i + d][j + d], arr[i][j + d])
    arr[i + k][j + k] = add_random(arr[i + k][j + k], rand)


def diamond_step(arr, i, j, d, rand):
    k = d // 2

    if i - k < 0:
        arr[i][j + k] = mid(arr[i][j], arr[i + k][j + k], arr[i][j + d])
    else:
        arr[i][j + k] = mid(arr[i][j], arr[i + k][j + k], arr[i][j + d], arr[i - k][j + k])
    arr[i][j + k] = add_random(arr[i][j + k], rand)

    if j + d + k >= len(arr):
        arr[i + k][j + d] = mid(arr[i][j + d], arr[i + k][j + k], arr[i + d][j + d])
    else:
        arr[i + k][j + d] = mid(arr[i][j + d], arr[i + k][j + k], arr[i + d][j + d], arr[i + k][j + d + k])
    arr[i + k][j + d] = add_random(arr[i + k][j + d], rand)

    if i + d + k >= len(arr):
        arr[i + d][j + k] = mid(arr[i + d][j + d], arr[i + k][j + k], arr[i + d][j])
    else:
        arr[i + d][j + k] = mid(arr[i + d][j + d], arr[i + k][j + k], arr[i + d][j], arr[i + d + k][j + k])
    arr[i + d][j + k] = add_random(arr[i + d][j + k], rand)

    if j - k < 0:
        arr[i + k][j] = mid(arr[i][j], arr[i + k][j + k], arr[i + d][j])
    else:
        arr[i + k][j] = mid(arr[i][j], arr[i + k][j + k], arr[i + d][j], arr[i + k][j - k])
    arr[i + k][j] = add_random(arr[i + k][j], rand)


def diamond_square(arr, p1, p2, p3, p4, rand):
    start_len = len(arr)
    n = round(log(start_len - 1, 2))
    d = len(arr) - 1
    rand[0] *= 2**n
    rand[1] *= 2 ** n

    arr[0][0] = p1
    arr[0][-1] = p2
    arr[-1][-1] = p3
    arr[-1][0] = p4

    for g in range(n):
        for i in range(2**g):
            for j in range(2**g):
                square_step(arr, i * d, j * d, d, rand)
        for i in range(2 ** g):
            for j in range(2 ** g):
                diamond_step(arr, i * d, j * d, d, rand)

        d //= 2
        rand[0] /= 2
        rand[1] /= 2


def add_random(num, r):
    return num + uniform(-r[0], r[1])
