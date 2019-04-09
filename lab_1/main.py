from random import random
from tkinter import *
from tkinter import messagebox
from math import cos, sin, pi, sqrt, acos
import copy


# ==========FUNCTIONS==========

# Generates dots with parameters
def dot_generator(x_beg, x_end, y_beg, y_end, amount):
    dots = []

    for i in range(amount):
        x = random() * (x_end - x_beg) + x_beg
        y = random() * (y_end - y_beg) + y_beg
        dots.append([x, y])

    return dots


# Finds all triples and indexes, that don't lie on one line
def find_triples(dots):
    triples = []
    inds = []
    n = len(dots)

    for i in range(n - 2):
        for j in range(i + 1, n - 1, 1):
            for k in range(j + 1, n):
                if (dots[i][0] - dots[k][0]) * (dots[j][1] - dots[k][1]) - \
                                (dots[j][0] - dots[k][0]) * (dots[i][1] - dots[k][1]) != 0:
                    triples.append([dots[i], dots[j], dots[k]])
                    inds.append([i, j, k])

    return triples, inds


# Finds centers of circles built on triples
def find_centers(triples):
    centers = []

    for coord in triples:
        a = coord[0]
        b = coord[1]
        c = coord[2]
        d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
        ox = ((a[0] ** 2 + a[1] ** 2) * (b[1] - c[1]) + (b[0] ** 2 + b[1] ** 2) * (c[1] - a[1]) + (
        c[0] ** 2 + c[1] ** 2) * (a[1] - b[1])) / d
        oy = ((a[0] ** 2 + a[1] ** 2) * (c[0] - b[0]) + (b[0] ** 2 + b[1] ** 2) * (a[0] - c[0]) + (
        c[0] ** 2 + c[1] ** 2) * (b[0] - a[0])) / d

        centers.append([ox, oy])

    return centers


# Finds indexes of centers with min angle between them and OX
def find_nearest(ctr_1, ctr_2):
    ind_1 = -1  # index in 1st triples
    ind_2 = -1 # index in 2nd triples
    d_min_angle = 180

    

    
    
    #"""
    for i in range(len(ctr_1)):
        for j in range(len(ctr_2)):
            if ctr_1[i] != ctr_2[j]:
                
                if ctr_1[i][0] >= ctr_2[j][0]:
                    cen_for_ang = ctr_1[i]
                    cen_other = ctr_2[j]
                else:
                    cen_for_ang = ctr_2[j]
                    cen_other = ctr_1[i]

                cur_angle = acos(dist(cen_other, [cen_for_ang[0], cen_other[1]]) / dist(cen_other, cen_for_ang))

                d_cur_angle = cur_angle * 180 / pi
                    
                if d_cur_angle < d_min_angle:
                    d_min_angle = d_cur_angle
                    ind_1 = i
                    ind_2 = j
    #"""
    """OLD
    for i in range(len(ctr_1)):
        for j in range(len(ctr_2)):
            if ctr_1[i] != ctr_2[j]:
                cur_dist = abs(ctr_1[i][1] - ctr_2[j][1])
                    
                if min_dist < 0:
                    min_dist = cur_dist
                    ind_1 = i
                    ind_2 = j
                elif cur_dist < min_dist:
                    min_dist = cur_dist
                    ind_1 = i
                    ind_2 = j
    """


    return ind_1, ind_2


# Масштабирует, переносит, и рисует картинку
def draw_pic(circle_1, circle_2, can, can_x, can_y, clr_1, clr_2):
    new_circle_1 = copy.deepcopy(circle_1)
    new_circle_2 = copy.deepcopy(circle_2)

    can_min_x = 50
    can_max_x = can_x - 50
    can_min_y = 50
    can_max_y = can_y - 50
    can_len_x = can_max_x - can_min_x
    can_len_y = can_max_y - can_min_y
    can_ox = can_x / 2 # центр зоны отображения
    can_oy = can_y / 2

    # Находим радиусы окружностей
    r1 = dist(new_circle_1[2], new_circle_1[0][0])
    r2 = dist(new_circle_2[2], new_circle_2[0][0])

    # Находим размер картинки
    min_x = min(new_circle_1[2][0] - r1, new_circle_2[2][0] - r2)
    min_y = min(new_circle_1[2][1] - r1, new_circle_2[2][1] - r2)
    max_x = max(new_circle_1[2][0] + r1, new_circle_2[2][0] + r2)
    max_y = max(new_circle_1[2][1] + r1, new_circle_2[2][1] + r2)

    # Длины сторон картинки
    len_x = max_x - min_x
    len_y = max_y - min_y

    # Центр картинки
    ox = min_x + len_x / 2
    oy = min_y + len_y / 2

    # Коэффицент масштабирования
    if len_x >= len_y:
        k = can_len_x / len_x
    else:
        k = can_len_y / len_y

    #'''
    # Масштабирование, центр масштабирования - центр изображения
    scale(new_circle_1, ox, oy, k)
    scale(new_circle_2, ox, oy, k)

    # Обновление радиусов
    r1 = dist(new_circle_1[2], new_circle_1[0][0])
    r2 = dist(new_circle_2[2], new_circle_2[0][0])

    # Перенос в область отображения
    dx = ox - can_ox
    dy = oy - can_oy
    move(new_circle_1, dx, dy)
    move(new_circle_2, dx, dy)
    #'''

    # РИСОВАНИЕ в исходной системе координат
    """
    # Рисуем ось по середине соединяющего отрезка
    axis_y = new_circle_1[2][1] + (new_circle_2[2][1] - new_circle_1[2][1]) / 2
    axis_x = new_circle_1[2][0] + (new_circle_2[2][0] - new_circle_1[2][0]) / 2
    can.create_line(0, axis_y, 800, axis_y, fill="lightgrey", arrow=LAST, arrowshape=(12, 15, 6))

    # Рисуем угол
    if new_circle_1[2][0] >= new_circle_2[2][0]:
        cen_for_ang = new_circle_1[2]
    else:
        cen_for_ang = new_circle_2[2]
    angle = acos(dist([axis_x, axis_y], [cen_for_ang[0], axis_y]) / dist([axis_x, axis_y], cen_for_ang))

    if cen_for_ang[1] > axis_y:
        d_angle = -angle * 180 / pi
    else:
        d_angle = angle * 180 / pi

    if dist(new_circle_1[2], new_circle_2[2]) < 60:
        angle_r = (dist(new_circle_1[2], new_circle_2[2]) - 5) / 2
    else:
        angle_r = 30

    part_circle([axis_x, axis_y], angle_r, d_angle, can)
    can.create_text(axis_x + 30, axis_y - 30, text="%.3f°" % abs(d_angle))

    # Рисуем отрезок, соединяющий центры
    can.create_line(new_circle_1[2][0], new_circle_1[2][1], new_circle_2[2][0], new_circle_2[2][1])
    draw_dot([new_circle_1[2][0], new_circle_1[2][1]], "grey", can)
    draw_dot([new_circle_2[2][0], new_circle_2[2][1]], "grey", can)

    # Рисуем окружности
    can.create_oval(new_circle_1[2][0] - r1, new_circle_1[2][1] - r1, new_circle_1[2][0] + r1, new_circle_1[2][1] + r1, outline=clr_1)
    can.create_oval(new_circle_2[2][0] - r2, new_circle_2[2][1] - r2, new_circle_2[2][0] + r2, new_circle_2[2][1] + r2, outline=clr_2)

    # Рисуем точки и их координаты
    for i in range(len(circle_1[0])):
        draw_dot(new_circle_1[0][i], "blue", can)
        can.create_text(new_circle_1[0][i][0] + 10, new_circle_1[0][i][1] - 10,
                        text="%s (%.3f, %.3f)" % (circle_1[1][i] + 1, circle_1[0][i][0], circle_1[0][i][1]))
    for i in range(len(circle_2[0])):
        draw_dot(new_circle_2[0][i], "red", can)
        can.create_text(new_circle_2[0][i][0] + 10, new_circle_2[0][i][1] - 10,
                        text="%s (%.3f, %.3f)" % (circle_2[1][i] + 1, circle_2[0][i][0], circle_2[0][i][1]))
    """

    # РИСОВАНИЕ в декартовой системе координат
    # Рисуем ось по середине соединяющего отрезка
    axis_y = can_y - (new_circle_1[2][1] + (new_circle_2[2][1] - new_circle_1[2][1]) / 2)
    axis_x = new_circle_1[2][0] + (new_circle_2[2][0] - new_circle_1[2][0]) / 2
    can.create_line(0, axis_y, 800, axis_y, fill="lightgrey", arrow=LAST, arrowshape=(12, 15, 6))

    # Рисуем угол
    if new_circle_1[2][0] >= new_circle_2[2][0]:
        cen_for_ang = new_circle_1[2]
    else:
        cen_for_ang = new_circle_2[2]
    angle = acos(dist([axis_x, axis_y], [cen_for_ang[0], axis_y]) / dist([axis_x, axis_y], [cen_for_ang[0], 800 - cen_for_ang[1]]))

    if 800 - cen_for_ang[1] > axis_y:
        d_angle = -angle * 180 / pi
    else:
        d_angle = angle * 180 / pi

    if dist(new_circle_1[2], new_circle_2[2]) < 60:
        angle_r = (dist(new_circle_1[2], new_circle_2[2]) - 5) / 2
    else:
        angle_r = 30

    part_circle([axis_x, axis_y], angle_r, d_angle, can)
    can.create_text(axis_x + 30, axis_y - 30, text="%.3f°" % abs(d_angle), font="Arial 18")

    # Рисуем отрезок, соединяющий центры
    can.create_line(new_circle_1[2][0], can_y - new_circle_1[2][1], new_circle_2[2][0], can_y - new_circle_2[2][1])
    draw_dot([new_circle_1[2][0], can_y - new_circle_1[2][1]], "grey", can)
    draw_dot([new_circle_2[2][0], can_y - new_circle_2[2][1]], "grey", can)

    # Рисуем окружности
    can.create_oval(new_circle_1[2][0] - r1, can_y - (new_circle_1[2][1] - r1), new_circle_1[2][0] + r1, can_y - (new_circle_1[2][1] + r1),
                    outline=clr_1)
    can.create_oval(new_circle_2[2][0] - r2, can_y - (new_circle_2[2][1] - r2), new_circle_2[2][0] + r2, can_y - (new_circle_2[2][1] + r2),
                    outline=clr_2)

    # Рисуем точки и их координаты
    for i in range(len(circle_1[0])):
        draw_dot([new_circle_1[0][i][0], can_y - new_circle_1[0][i][1]], "blue", can)
        can.create_text(new_circle_1[0][i][0] + 10, (can_y - new_circle_1[0][i][1]) - 10,
                        text="%s (%.3f, %.3f)" % (circle_1[1][i] + 1, circle_1[0][i][0], circle_1[0][i][1]))
    for i in range(len(circle_2[0])):
        draw_dot([new_circle_2[0][i][0], can_y - new_circle_2[0][i][1]], "red", can)
        can.create_text(new_circle_2[0][i][0] + 10, (can_y - new_circle_2[0][i][1]) - 10,
                        text="%s (%.3f, %.3f)" % (circle_2[1][i] + 1, circle_2[0][i][0], circle_2[0][i][1]))





# ==========SECONDARY FUNCTIONS==========
# Scales circle
def scale(circle, ox, oy, k):
    for couple in circle[0]:
        couple[0] = (couple[0] - ox) * k + ox
        couple[1] = (couple[1] - oy) * k + oy
    circle[2][0] = (circle[2][0] - ox) * k + ox
    circle[2][1] = (circle[2][1] - oy) * k + oy

# Moves circle
def move(circle, dx, dy):
    for couple in circle[0]:
        couple[0] -= dx
        couple[1] -= dy
    circle[2][0] -= dx
    circle[2][1] -= dy

# Cos(angle in degrees)
def d_cos(a):
    return cos(a * pi / 180)

# Draws part of circle, inside two angles
def part_circle(centre, r, angle, can):
    num = int(abs(angle) / 45 * r)
    if num == 0:
        return -1
    step = (r - d_cos(angle) * r) / num
    x = r
    y = 0

    for i in range(num):
        old_coord = [x, y]

        x -= step
        if angle >= 0:
            y = -sqrt(r**2 - x**2)
        else:
            y = sqrt(r**2 - x**2)

        new_coord = [x, y]
        can.create_line(centre[0] + old_coord[0], centre[1] + old_coord[1],
                        centre[0] + new_coord[0], centre[1] + new_coord[1])

# Draws dot on x, y
def draw_dot(a, color, can):
    can.create_oval(a[0] - 2, a[1] - 2, a[0] + 2, a[1] + 2, fill=color)

# Finds distance between 2 points (a=[x0,y0], b=[x1,y1])
def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)

# Prints warning message
def mes(text):
    messagebox.showinfo("Внимание", text)


def print_dots(dots_1, dots_2):
    print(dots_1)
    print(dots_2)

# ==========GUI FUNCTIONS==========
def build_scene(can, dots_1, dots_2):
    can.delete("all")

    #dots_1 = dot_generator(-1000, 1000, -1000, 1000, 5)
    #dots_2 = dot_generator(-1000, 1000, -1000, 1000, 5)

    if len(dots_1) < 3:
        mes("В первом множестве недостаточно точек")
        return -1
    if len(dots_2) < 3:
        mes("Во втором множестве недостаточно точек")
        return -2

    triples_1, triples_i_1 = find_triples(dots_1)
    triples_2, triples_i_2 = find_triples(dots_2)

    if len(triples_1) == 0:
        mes("В первом множестве все точки лежат на одной прямой")
        return -3
    if len(triples_2) == 0:
        mes("Во втором множестве все точки лежат на одной прямой")
        return -4

    centers_1 = find_centers(triples_1)
    centers_2 = find_centers(triples_2)

    ind_1, ind_2 = find_nearest(centers_1, centers_2)
    if ind_1 == -1 and ind_2 == -1:
        mes("Все центры окружностей в обоих множествах совпадают")
        return -5

    circle_1 = [triples_1[ind_1], triples_i_1[ind_1], centers_1[ind_1]]
    circle_2 = [triples_2[ind_2], triples_i_2[ind_2], centers_2[ind_2]]

    print(circle_1)
    print(circle_2)

    color_1 = "blue"
    color_2 = "red"
    draw_pic(circle_1, circle_2, can, 800, 800, color_1, color_2)

# Добавление точки в массив и в listbox
def add_dot(dots_1, dots_2, pl, x, y, lb1, lb2):
    try:
        pl = int(pl.get())
        x = float(x.get())
        y = float(y.get())
    except ValueError:
        messagebox.showinfo("Внимание", "Неверные данные!")
        return -1

    if pl == 1:
        dots = dots_1
        lb = lb1
    elif pl == 2:
        dots = dots_2
        lb = lb2
    else:
        messagebox.showinfo("Внимание", "Введите правильный номер множества: 1/2")
        return -2

    for i in range(len(dots)):
        if dots[i][0] == x and dots[i][1] == y:
            messagebox.showinfo("Внимание", "Такая точка уже содержится в множестве")
            return -3

    dots.append([x, y])
    lb.insert(len(dots), lb_line(len(dots), dots[-1][0], dots[-1][1], 25))

# Возвращает строку для записи в listbox
def lb_line(i, x, y, n):
    x = "%.3f" % x
    y = "%.3f" % y
    return str(i) + " " * int((n - 1) / 2 - len(x)) + x + " " * int((n - 1) / 2 - len(y)) + y

# Удаляет точку из массива и из listbox
def delete(dots_1, dots_2, lb_1, lb_2):
    if len(lb_1.curselection()) > 0 and lb_1.curselection()[0] > 0:
        dots = dots_1
        lb = lb_1
    elif len(lb_2.curselection()) > 0 and lb_2.curselection()[0] > 0:
        dots = dots_2
        lb = lb_2
    else:
        messagebox.showinfo("Внимание", "Выберете точку, которую хотите удалить")
        return -1

    ind = lb.curselection()[0]

    dots.pop(ind - 1)

    for i in range(len(lb.get(ind, END)) - 1):
        lb.delete(ind + i + 1)
        lb.insert(ind + i + 1, lb_line(ind + i, dots[ind + i - 1][0], dots[ind + i - 1][1], 25))
    lb.delete(ind)

# Удаляет все точки из выбранного множества или из обоих множеств
def delete_all(dots_1, dots_2, lb_1, lb_2):
    if len(lb_1.curselection()) == 0 and len(lb_2.curselection()) == 0:
        del_all = 1
    elif len(lb_1.curselection()) > 0:
        dots = dots_1
        lb = lb_1
        del_all = 0
    else:
        dots = dots_2
        lb = lb_2
        del_all = 0

    if del_all == 1:
        dots_1.clear()
        dots_2.clear()
        lb_1.delete(1, END)
        lb_2.delete(1, END)
    else:
        dots.clear()
        lb.delete(1, END)

# Изменяет координаты выбранной точки
def change(dots_1, dots_2, x, y, lb_1, lb_2):
    try:
        x = float(x.get())
        y = float(y.get())
    except ValueError:
        mes("Неверные данные!")
        return -1

    if len(lb_1.curselection()) > 0 and lb_1.curselection()[0] > 0:
        dots = dots_1
        lb = lb_1
    elif len(lb_2.curselection()) > 0 and lb_2.curselection()[0] > 0:
        dots = dots_2
        lb = lb_2
    else:
        mes("Выберете точку, которую хотите изменить")
        return -2

    for i in range(len(dots)):
        if dots[i][0] == x and dots[i][1] == y:
            mes("Такая точка уже содержится в множестве")
            return -3

    ind = lb.curselection()[0]

    dots[ind - 1][0] = x
    dots[ind - 1][1] = y

    lb.delete(ind)
    lb.insert(ind, lb_line(ind, dots[ind - 1][0], dots[ind - 1][1], 25))


# ==========MAIN==========
def main():
    root = Tk()
    can_co = 800
    root.geometry(str(can_co + 320) + "x" + str(can_co))
    root.title("KG-1")
    EntryW = 10
    Font = "Arial 14"
    Can = Canvas(root, height=can_co, width=can_co, bg='white')

    dots_1 = []#dot_generator(-1000, 1000, -1000, 1000, 5)
    dots_2 = []#dot_generator(-1000, 1000, -1000, 1000, 5)

    # Frames
    WorkSpace = Frame(root)
    Dots1 = Frame(WorkSpace, relief=GROOVE, bd=1)
    Dots2 = Frame(WorkSpace, relief=GROOVE, bd=1)
    Add = Frame(WorkSpace)
    Delete = Frame(WorkSpace)
    Change = Frame(WorkSpace)

    # Dots1
    Dots1Name = Label(Dots1, text="Множество 1", font=Font, fg="blue").grid(row=0, column=0)
    Dots1LB = Listbox(Dots1, width=25, activestyle="none", selectbackground="grey")
    Dots1LB.grid(row=1, column=0)
    Dots1LB.insert(1, "№" + " " * 12 + "x" + " " * 12 + "y")

    Dots1.grid(row=0, column=0)

    # Dots2
    Dots2Name = Label(Dots2, text="Множество 2", font=Font, fg="red").grid(row=0, column=0)
    Dots2LB = Listbox(Dots2, width=25, activestyle="none", selectbackground="grey")
    Dots2LB.grid(row=1, column=0)
    Dots2LB.insert(1, "№" + " " * 12 + "x" + " " * 12 + "y")

    Dots2.grid(row=0, column=1)

    # Add
    AddPlVar = IntVar()
    AddXVar = StringVar()
    AddYVar = StringVar()

    AddName = Label(Add, text="Добавить:", font=Font).grid(row=0, column=1, columnspan=2)
    AddPlRB1 = Radiobutton(Add, text="Множество 1", variable=AddPlVar, value=1, font=Font)
    AddPlRB2 = Radiobutton(Add, text="Множество 2", variable=AddPlVar, value=2, font=Font).grid(row=1, column=2, columnspan=2)
    AddPlRB1.select()
    AddX = Label(Add, text="X:", font=Font).grid(row=2, column=0)
    AddY = Label(Add, text="Y:", font=Font).grid(row=2, column=2)

    AddXEntry = Entry(Add, width=EntryW, textvariable=AddXVar).grid(row=2, column=1)
    AddYEntry = Entry(Add, width=EntryW, textvariable=AddYVar).grid(row=2, column=3)

    AddButton = Button(Add, text="Добавить", font=Font, command=lambda: add_dot(dots_1, dots_2, AddPlVar, AddXVar,
                       AddYVar, Dots1LB, Dots2LB)).grid(row=3, column=1, columnspan=2)
    AddPlRB1.grid(row=1, column=0, columnspan=2)

    Add.grid(row=1, column=0, columnspan=2)

    # Delete
    DeletePlVar = StringVar()
    DeleteIndVar = StringVar()

    DeleteName = Label(Delete, text="Удалить:", font=Font).grid(row=0, column=1, columnspan=2)

    DeleteButton = Button(Delete, text="Удалить", font=Font, command=lambda: delete(dots_1, dots_2, Dots1LB,
                          Dots2LB)).grid(row=1, column=0, columnspan=2)
    DeleteAllButton = Button(Delete, text="Удалить все", font=Font, command=lambda: delete_all(dots_1, dots_2,
                             Dots1LB, Dots2LB)).grid(row=1, column=2, columnspan=2)

    Delete.grid(row=2, column=0, columnspan=2)

    # Change
    ChangePlVar = StringVar()
    ChangeIndVar = StringVar()
    ChangeXVar = StringVar()
    ChangeYVar = StringVar()

    ChangeName = Label(Change, text="Изменить точку:", font=Font).grid(row=0, column=1, columnspan=2)
    ChangeX = Label(Change, text="Новый X:", font=Font).grid(row=1, column=0)
    ChangeY = Label(Change, text="Новый Y:", font=Font).grid(row=1, column=2)

    ChangeXEntry = Entry(Change, width=EntryW, textvariable=ChangeXVar).grid(row=1, column=1)
    ChangeYEntry = Entry(Change, width=EntryW, textvariable=ChangeYVar).grid(row=1, column=3)

    ChangeButton = Button(Change, text="Изменить", font=Font, command=lambda: change(dots_1, dots_2, ChangeXVar,
                          ChangeYVar, Dots1LB, Dots2LB)).grid(row=2, column=1, columnspan=2)

    Change.grid(row=3, column=0, columnspan=2)

    # In WorkFrame
    DrawButton = Button(WorkSpace, text="Нарисовать", font=Font, command=lambda: build_scene(Can, dots_1,
                        dots_2)).grid(row=4, column=0, columnspan=2)


    Can.grid(row=0, column=0)
    WorkSpace.grid(row=0, column=1, sticky="nsew")

    WorkSpace.rowconfigure(0, weight=1)
    WorkSpace.rowconfigure(1, weight=1)
    WorkSpace.rowconfigure(2, weight=1)
    WorkSpace.rowconfigure(3, weight=1)
    WorkSpace.rowconfigure(4, weight=1)

    root.mainloop()

main()

