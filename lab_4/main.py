import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.colorchooser import askcolor

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from typing import NamedTuple
from algorithms import *
from testing import time_test

# Структура Круг
class Circle(NamedTuple):
    xc: int
    yc: int
    r: int
    color: str
    alg: int


# Структура Эллипс
class Ellipse(NamedTuple):
    xc: int
    yc: int
    a: int
    b: int
    color: str
    alg: int


# Класс приложения
class Kg4App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)

        options_size = 336 # const
        can_x = args[0] - options_size
        can_y = args[1]

        tk.Tk.title(self, "KG-4")
        tk.Tk.geometry(self, str(can_x + options_size) + "x" + str(can_y))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Класс главной страницы
class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.color_bg = "#fff"
        self.color_line = "#000000"
        self.color_pen = self.color_line
        self.objects = []
        self.res = []

        # TABS
        self.work = tk.Frame(self)
        self.tab_parent = ttk.Notebook(self.work, height=140)
        self.tab1 = ttk.Frame(self.tab_parent)
        self.tab2 = ttk.Frame(self.tab_parent)
        self.tab3 = ttk.Frame(self.tab_parent)
        self.tab4 = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.tab1, text="Окружность")
        self.tab_parent.add(self.tab2, text="Эллипс")
        self.tab_parent.add(self.tab3, text="Спектр окр.")
        self.tab_parent.add(self.tab4, text="Спектр элл.")
        self.tab_parent.grid(row=0, column=0, columnspan=2)

        self.var1_1 = tk.StringVar()
        self.var2_1 = tk.StringVar()
        self.var3_1 = tk.StringVar()
        self.var4_1 = tk.StringVar()
        self.var1_2 = tk.StringVar()
        self.var2_2 = tk.StringVar()
        self.var3_2 = tk.StringVar()
        self.var4_2 = tk.StringVar()
        self.var1_3 = tk.StringVar()
        self.var2_3 = tk.StringVar()
        self.var3_3 = tk.StringVar()
        self.var4_3 = tk.StringVar()
        self.var1_4 = tk.StringVar()
        self.var2_4 = tk.StringVar()
        self.var3_4 = tk.StringVar()
        self.var4_4 = tk.StringVar()

        # Tab 1
        self.e_w = 20
        self.tab1_label_1 = ttk.Label(self.tab1, text="X:").grid(row=0, column=0)
        self.tab1_label_2 = ttk.Label(self.tab1, text="   Y:").grid(row=0, column=2)
        self.tab1_label_3 = ttk.Label(self.tab1, text="Радиус:").grid(row=1, column=0)
        self.tab1_entry_x = ttk.Entry(self.tab1, textvariable=self.var1_1, width=self.e_w).grid(row=0, column=1)
        self.tab1_entry_y = ttk.Entry(self.tab1, textvariable=self.var2_1, width=self.e_w).grid(row=0, column=3)
        self.tab1_entry_r = ttk.Entry(self.tab1, textvariable=self.var3_1, width=self.e_w).grid(row=1, column=1)
        self.tab1.grid_rowconfigure(0, weight=1)
        self.tab1.grid_rowconfigure(1, weight=1)
        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_columnconfigure(1, weight=1)

        # Tab 2
        self.tab2_label_1 = ttk.Label(self.tab2, text="X:").grid(row=0, column=0)
        self.tab2_label_2 = ttk.Label(self.tab2, text="   Y:").grid(row=0, column=2)
        self.tab2_label_3 = ttk.Label(self.tab2, text="A:").grid(row=1, column=0)
        self.tab2_label_4 = ttk.Label(self.tab2, text="   B:").grid(row=1, column=2)
        self.tab2_entry_x = ttk.Entry(self.tab2, textvariable=self.var1_2, width=self.e_w).grid(row=0, column=1)
        self.tab2_entry_y = ttk.Entry(self.tab2, textvariable=self.var2_2, width=self.e_w).grid(row=0, column=3)
        self.tab2_entry_a = ttk.Entry(self.tab2, textvariable=self.var3_2, width=self.e_w).grid(row=1, column=1)
        self.tab2_entry_b = ttk.Entry(self.tab2, textvariable=self.var4_2, width=self.e_w).grid(row=1, column=3)
        self.tab2.grid_rowconfigure(0, weight=1)
        self.tab2.grid_rowconfigure(1, weight=1)
        self.tab2.grid_columnconfigure(0, weight=1)
        self.tab2.grid_columnconfigure(1, weight=1)

        # Tab 3
        self.e_w = 10
        self.tab3_label_1 = ttk.Label(self.tab3, text="Начальный радиус:").grid(row=0, column=0)
        self.tab3_label_2 = ttk.Label(self.tab3, text="Шаг:").grid(row=1, column=0)
        self.tab3_label_3 = ttk.Label(self.tab3, text="   Количество:").grid(row=1, column=2)
        self.tab3_entry_r = ttk.Entry(self.tab3, textvariable=self.var1_3, width=self.e_w).grid(row=0, column=1)
        self.tab3_entry_step = ttk.Entry(self.tab3, textvariable=self.var2_3, width=self.e_w).grid(row=1, column=1)
        self.tab3_entry_amount = ttk.Entry(self.tab3, textvariable=self.var3_3, width=self.e_w).grid(row=1, column=3)
        self.tab3.grid_rowconfigure(0, weight=1)
        self.tab3.grid_rowconfigure(1, weight=1)
        self.tab3.grid_columnconfigure(0, weight=1)
        self.tab3.grid_columnconfigure(1, weight=1)

        # Tab 4
        self.tab4_label_1 = ttk.Label(self.tab4, text="Начальное A:").grid(row=0, column=0)
        self.tab4_label_2 = ttk.Label(self.tab4, text="   Начальное B:").grid(row=0, column=2)
        self.tab4_label_3 = ttk.Label(self.tab4, text="Шаг по A:").grid(row=1, column=0)
        self.tab4_label_4 = ttk.Label(self.tab4, text="   Количество:").grid(row=1, column=2)
        self.tab4_entry_x = ttk.Entry(self.tab4, textvariable=self.var1_4, width=self.e_w).grid(row=0, column=1)
        self.tab4_entry_y = ttk.Entry(self.tab4, textvariable=self.var2_4, width=self.e_w).grid(row=0, column=3)
        self.tab4_entry_a = ttk.Entry(self.tab4, textvariable=self.var3_4, width=self.e_w).grid(row=1, column=1)
        self.tab4_entry_b = ttk.Entry(self.tab4, textvariable=self.var4_4, width=self.e_w).grid(row=1, column=3)
        self.tab4.grid_rowconfigure(0, weight=1)
        self.tab4.grid_rowconfigure(1, weight=1)
        self.tab4.grid_columnconfigure(0, weight=1)
        self.tab4.grid_columnconfigure(1, weight=1)

        self.button_line_color = ttk.Button(self.work, text="Цвет линии",
                                            command=lambda: get_color_line(self)).grid(row=1, column=0)
        self.label_line_color = tk.Label(self.work, bg=self.color_line, width=20)
        self.label_line_color.grid(row=1, column=1)
        self.button_bg_color = ttk.Button(self.work, text="Цвет фона",
                                          command=lambda: get_color_bg(self)).grid(row=2, column=0)
        self.label_bg_color = tk.Label(self.work, bg=self.color_bg, width=20)
        self.label_bg_color.grid(row=2, column=1)

        self.ch_var = tk.IntVar()
        self.ch_button_color = ttk.Checkbutton(self.work, text="Рисовать цветом фона", variable=self.ch_var)
        self.ch_var.set(0)
        self.ch_button_color.grid(row=3, column=0)

        self.list_alg = ["Каноническое уравнение", "Параметрическое уравнение", "Алгоритм Брезенхема",
                    "Метод средней точки", "Библиотечный метод"]
        self.combobox_alg = ttk.Combobox(self.work, width=25, values=self.list_alg, state="readonly")
        self.combobox_alg.current(0)
        self.combobox_alg.grid(row=4, column=0)
        self.button_test = ttk.Button(self.work, text="Временные характеристики",
                                 command=lambda: controller.show_frame(GraphPage)).grid(row=4, column=1)
        self.button_draw = ttk.Button(self.work, text="Нарисовать",
                                 command=lambda: draw(self)).grid(row=5, column=0)
        self.button_clear = ttk.Button(self.work, text="Очистить",
                                  command=lambda: clear(self) ).grid(row=5, column=1)

        self.work.pack(side=tk.RIGHT)
        self.canvas = tk.Canvas(self, bg=self.color_bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)


# Класс страницы с графиком
class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Вернуться",
                             command=lambda: controller.show_frame(MainPage))
        button1.pack()


        res = time_test(10000)

        f = Figure(figsize=(5, 5), dpi=100)

        plt = f.add_subplot(111)
        plt.plot(res[4], res[0], label="Каноническое уравнение")
        plt.plot(res[4], res[1], label="Параметрическое уравнение")
        plt.plot(res[4], res[2], label="Алгоритм Брезенхема")
        plt.plot(res[4], res[3], label="Метод средней точки")

        plt.set_xlabel("Радиус")
        plt.set_ylabel("Время")
        plt.set_title("Временные характеристики окружностей")

        plt.legend()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        #toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)


# Выводит на экран предупреждение с текстом
def mes(text):
    messagebox.showinfo("Внимание", text)


# Получаем цвет линии
def get_color_line(self):
    color = askcolor()[1]

    if color:
        self.color_line = color
        self.label_line_color.configure(bg=color)


# Получаем цвет фона и сразу его заменяем
def get_color_bg(self):
    color = askcolor()[1]

    if color:
        self.color_bg = color
        self.label_bg_color.configure(bg=color)

        self.canvas.configure(bg=self.color_bg)


# Очищаем холст
def clear(self):
    #self.objects = []
    self.canvas.delete("all")
    self.canvas.configure(bg=self.color_bg)

    print("can: ", self.canvas.winfo_width(), self.canvas.winfo_height())


# Получаем данные и формируем объект
def draw(self):
    tab = self.tab_parent.index(self.tab_parent.select())

    # Получаем данные
    if tab == 0:
        try:
            xc = int(self.var1_1.get())
            yc = int(self.var2_1.get())
            r = int(self.var3_1.get())
        except ValueError:
            mes("Неверные данные!")
            return -1
    elif tab == 1:
        try:
            xc = int(self.var1_2.get())
            yc = int(self.var2_2.get())
            a = int(self.var3_2.get())
            b = int(self.var4_2.get())
        except ValueError:
            mes("Неверные данные!")
            return -2
    elif tab == 2:
        try:
            r_beg = int(self.var1_3.get())
            step = int(self.var2_3.get())
            amount = int(self.var3_3.get())
        except ValueError:
            mes("Неверные данные!")
            return -3
    elif tab == 3:
        try:
            a_beg = int(self.var1_4.get())
            b_beg = int(self.var2_4.get())
            a_step = int(self.var3_4.get())
            amount = int(self.var4_4.get())
        except ValueError:
            mes("Неверные данные!")
            return -4

    if int(self.ch_var.get()) == 1:
        color = self.color_bg
    else:
        color = self.color_line
    alg = self.combobox_alg.current()

    can_x = self.canvas.winfo_width()
    can_y = self.canvas.winfo_height()

    if tab == 0:
        circle = Circle(xc, yc, r, color, alg)
        draw_func(self, circle)
    elif tab == 1:
        ellipse = Ellipse(xc, yc, a, b, color, alg)
        draw_func(self, ellipse)
    elif tab == 2:
        for i in range(amount):
            circle = Circle(can_x // 2, can_y // 2, r_beg, color, alg)
            draw_func(self, circle)
            r_beg += step

    elif tab == 3:
        b_step = round(b_beg / a_beg * a_step)
        for i in range(amount):
            ellipse = Ellipse(can_x // 2, can_y // 2, a_beg, b_beg, color, alg)
            draw_func(self, ellipse)
            a_beg += a_step
            b_beg += b_step

    for o in self.objects:
        draw_func(self, o)


# Отправляем объект на рисовку в нужный алгоритм
def draw_func(self, obj):
    self.color_pen = obj.color

    if type(obj) == Circle:
        if obj.alg == 0:
            draw_circle_canon(self, obj.xc, obj.yc, obj.r)
        elif obj.alg == 1:
            draw_circle_param(self, obj.xc, obj.yc, obj.r)
        elif obj.alg == 2:
            draw_circle_br(self, obj.xc, obj.yc, obj.r)
        elif obj.alg == 3:
            draw_circle_mid(self, obj.xc, obj.yc, obj.r)
        elif obj.alg == 4:
            draw_circle_std(self, obj.xc, obj.yc, obj.r)
    elif type(obj) == Ellipse:
        if obj.alg == 0:
            draw_ellipse_canon(self, obj.xc, obj.yc, obj.a, obj.b)
        elif obj.alg == 1:
            draw_ellipse_param(self, obj.xc, obj.yc, obj.a, obj.b)
        elif obj.alg == 2:
            draw_ellipse_br(self, obj.xc, obj.yc, obj.a, obj.b)
        elif obj.alg == 3:
            draw_ellipse_mid(self, obj.xc, obj.yc, obj.a, obj.b)
        elif obj.alg == 4:
            draw_ellipse_std(self, obj.xc, obj.yc, obj.a, obj.b)


if __name__ == '__main__':
    app = Kg4App(1000, 600)
    app.mainloop()
