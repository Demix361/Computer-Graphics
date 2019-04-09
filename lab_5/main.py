import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from operator import itemgetter

from funcs import *


# Main window class
class Kg5App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)

        def click_add(event):
            if self.ctrl_pressed == 0:
                add(self, event.x, event.y)
            else:
                if len(self.figs) > self.fig_n:
                    x_prev = self.figs[self.fig_n][-1][0]
                    y_prev = self.figs[self.fig_n][-1][1]

                    x = event.x - x_prev
                    y = event.y - y_prev

                    if abs(y) >= abs(x):
                        add(self, x_prev, event.y)
                    else:
                        add(self, event.x, y_prev)
                else:
                    add(self, event.x, event.y)


        def click_end(event):
            if len(self.figs) > self.fig_n:
                if len(self.figs[self.fig_n]) <= 2:
                    clear(self, "tag" + str(self.fig_n))
                else:
                    end(self)

        def press_key(event):
            if event.keysym == "Control_L":
                if self.ctrl_pressed == 0:
                    self.ctrl_pressed = 1

        def release_key(event):
            if event.keysym == "Control_L":
                if self.ctrl_pressed == 1:
                    self.ctrl_pressed = 0

        def moving_line(event):
            self.in_canvas = 1

            if self.drawing == 1:
                if self.ctrl_pressed == 0:
                    cur_pos = (event.x, event.y)

                    self.canvas.delete("new")
                    self.canvas.create_line(self.figs[self.fig_n][-1], cur_pos, fill=self.bd_color, tag="new")
                else:
                    x_prev = self.figs[self.fig_n][-1][0]
                    y_prev = self.figs[self.fig_n][-1][1]

                    x = event.x - x_prev
                    y = event.y - y_prev

                    if abs(y) >= abs(x):
                        cur_pos = (x_prev, event.y)
                    else:
                        cur_pos = (event.x, y_prev)

                    self.canvas.delete("new")
                    self.canvas.create_line(self.figs[self.fig_n][-1], cur_pos, fill=self.bd_color, tag="new")

        def in_window(event):
            if self.in_canvas == 0:
                self.canvas.delete("new")
            self.in_canvas = 0


        options_size = 300  # const
        can_x = args[0] - options_size
        can_y = args[1]

        tk.Tk.title(self, "KG-5")
        tk.Tk.geometry(self, str(can_x + options_size) + "x" + str(can_y))

        self.fill_color = "#42f4d1"
        self.bg_color = "#fff"
        self.bd_color = "#000000"

        self.fig_n = 0 # Количество многоугольников
        self.figs = [] # Хранит многоугольники
        self.ctrl_pressed = 0 # Нажат ли ctrl
        self.drawing = 0 # Отображать отрезок до курсора
        self.in_canvas = 0 # Курсор находитсся в canvas
        self.delay = 2 # Задержка
        self.edges = [] # Массив ребер
        self.process = None
        self.table_items = [] # Элементы таблицы


        self.work = ttk.Frame(self)


        self.table = ttk.Treeview(self.work, columns="X", height=10)
        self.table.heading("#0", text="X")
        self.table.heading("#1", text="Y")
        self.table.column("#0", width=150)
        self.table.column("#1", width=150)

        self.table.grid(row=0, column=0, sticky="ns")


        self.add = ttk.LabelFrame(self.work, text="Добавить новое ребро")

        self.var_x = tk.StringVar()
        self.var_y = tk.StringVar()

        self.label_x = ttk.Label(self.add, text="X точки:")
        self.label_x.grid(row=1, column=0)
        self.entry_x = ttk.Entry(self.add, textvariable = self.var_x, width=10)
        self.entry_x.grid(row=1, column=1)

        self.label_y = ttk.Label(self.add, text="Y точки:")
        self.label_y.grid(row=1, column=2)
        self.entry_y = ttk.Entry(self.add, textvariable=self.var_y, width=10)
        self.entry_y.grid(row=1, column=3)

        self.button_add = ttk.Button(self.add, text="Добавить", command=lambda: get_add(self))
        self.button_add.grid(row=2, column=0, columnspan=2)

        self.button_end = ttk.Button(self.add, text="Закончить", command=lambda: click_end(self))
        self.button_end.grid(row=2, column=2, columnspan=2)

        self.add.grid(row=1, column=0, sticky="nsew")
        self.add.grid_columnconfigure(0, weight=1)
        self.add.grid_columnconfigure(1, weight=1)
        self.add.grid_columnconfigure(2, weight=1)
        self.add.grid_columnconfigure(3, weight=1)


        self.color = ttk.LabelFrame(self.work, text="Выбор цвета")

        self.button_border = ttk.Button(self.color, text="Цвет границы",
                                        command=lambda: pick_color(self, "bd"))
        self.button_border.grid(row=0, column=0)

        self.label_bd = tk.Label(self.color, bg=self.bd_color, width=10)
        self.label_bd.grid(row=0, column=1)

        self.button_fill = ttk.Button(self.color, text="Цвет закраски",
                                        command=lambda: pick_color(self, "fill"))
        self.button_fill.grid(row=1, column=0)

        self.label_fill = tk.Label(self.color, bg=self.fill_color, width=10)
        self.label_fill.grid(row=1, column=1)

        self.color.grid(row=2, column=0, sticky="nsew")
        self.color.grid_columnconfigure(0, weight=1)
        self.color.grid_columnconfigure(1, weight=1)


        self.options = ttk.LabelFrame(self.work, text="Действия")

        self.button_clear = ttk.Button(self.options, text="Очистить", command=lambda: clear(self, "all"))
        self.button_clear.grid(row=0, column=0)

        self.button_fill = ttk.Button(self.options, text="Закрасить", command=lambda: fill(self))
        self.button_fill.grid(row=0, column=1)

        self.delay_var = tk.IntVar()
        self.delay_var.set(0)
        self.delay_cb = ttk.Checkbutton(self.options, text="Закрашивать с задержкой", variable=self.delay_var)
        self.delay_cb.grid(row=1, column=0, columnspan=2)

        self.delay_label = ttk.Label(self.options, text="Задержка (мс.)")
        self.delay_label.grid(row=2, column=0)

        self.delay_str = tk.StringVar()
        self.delay_str.set(str(self.delay))
        self.delay_entry = ttk.Entry(self.options, width=10, textvariable=self.delay_str)
        self.delay_entry.grid(row=2, column=1)

        self.options.grid(row=3, column=0, sticky="nsew")
        self.options.grid_columnconfigure(0, weight=1)
        self.options.grid_columnconfigure(1, weight=1)


        self.work.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self, bg=self.bg_color)
        tk.Tk.bind(self, "<KeyPress>", press_key)
        tk.Tk.bind(self, "<KeyRelease>", release_key)
        tk.Tk.bind(self, "<Motion>", in_window)
        self.canvas.bind("<Button-1>", click_add)
        self.canvas.bind("<Button-3>", click_end)
        self.canvas.bind("<Motion>", moving_line)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


# Calls functions for filling polygon
def fill(self):
    self.edges = get_edges(self.figs)
    if len(self.edges) < 3:
        mes("Недостаточно ребер")
        return -1

    intersections = get_intersections(self.edges)

    intersections.sort(key=itemgetter(1, 0))

    if int(self.delay_var.get()) == 1:
        try:
            self.delay = int(self.delay_str.get())
        except ValueError:
            mes("Неверная задержка.")
            return -2
        
        fill_delay(self, intersections)
    else:
        fill_figure(self, intersections)
        draw_edges(self)


# Picks color
def pick_color(self, name):
    color = askcolor()[1]
    print(color)

    if name == "bd":
        self.bd_color = color
        self.label_bd.configure(bg=color)
    elif name == "fill":
        self.fill_color = color
        self.label_fill.configure(bg=color)


# Creates window with warning
def mes(text):
    messagebox.showinfo("Внимание", text)


# Runs add with manual input
def get_add(self):
    try:
        x = int(self.var_x.get())
        y = int(self.var_y.get())
    except ValueError:
        mes("Неверные данные!")
        return -1

    add(self, x, y)


# Adds new dot and connects with previous
def add(self, x, y):
    if len(self.figs) <= self.fig_n:
        self.figs.append([])
        self.table_items.append([])
        
    self.figs[self.fig_n].append((x, y))
    self.table_items[self.fig_n].append(self.table.insert("", "end", text=str(x), values=(str(y))))

    if self.drawing == 0:
        self.drawing = 1

    if len(self.figs[self.fig_n]) > 1:
        self.canvas.create_line(self.figs[self.fig_n][-1],
                                self.figs[self.fig_n][-2], fill=self.bd_color, tag="tag"+str(self.fig_n))


# Connects last point with first
def end(self):
    if len(self.figs[self.fig_n]) > 2:
        self.canvas.create_line(self.figs[self.fig_n][-1],
                                self.figs[self.fig_n][0], fill=self.bd_color, tag="tag"+str(self.fig_n))

        self.table_items[self.fig_n].append(self.table.insert("", "end", text="==========", values="=========="))

        self.fig_n += 1

        self.drawing = 0
        self.canvas.delete("new")


# Clears obj and resets variables
def clear(self, obj):
    self.drawing = 0
    self.canvas.delete(obj)
    self.canvas.delete("new")
    if self.process is not None:
        self.canvas.after_cancel(self.process)
    self.pix_map = []
    self.edges = []

    if obj == "all":
        self.figs = []
        self.fig_n = 0
        self.table_items = []
        self.table.delete(*self.table.get_children())
    else:
        self.figs.pop()
        for item in self.table_items.pop():
            self.table.delete(item)


if __name__ == '__main__':
    app = Kg5App(1000, 600)
    app.mainloop()
