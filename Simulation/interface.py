import math
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from source import Solution


class GUI:
    def __init__(self, master):
        master.title("Моделирование случайной величины")
        master.geometry('1900x1000')
        master["bg"] = "#B0E0E6"
        self.master = master
        self.label_p = Label(master, text="Введите значение p = ", font="Consolas 14")
        self.label_n = Label(master, text="Введите значение n = ", font="Consolas 14")
        self.probability_value = Entry(master, font="Consolas 14", width=15, background='#1E90FF')
        self.n_value = Entry(master, font="Consolas 14", width=15, background='#1E90FF')
        self.button = Button(master, text="Построить", bd=2, width=20, height=2, background='#00FFFF',
                             command=self.create_model)

        self.fig, self.ax = plt.subplots(1, 1)
        self.fig.set_size_inches(11, 8)
        self.ax.grid(True)
        self.ax.set_facecolor("#00FA9A")
        self.ax.set_title("График функции распределения")
        chart = FigureCanvasTkAgg(self.fig, master)
        NavigationToolbar2Tk(chart).place(x=1320, y=950)
        chart.get_tk_widget().place(x=460, y=190)

        self.button.place(x=100, y=60)
        self.label_p.place(x=0, y=0)
        self.label_n.place(x=0, y=25)
        self.probability_value.place(x=218, y=0)
        self.n_value.place(x=218, y=25)

    def create_model(self):
        self.ax.clear()
        self.ax.set_title("График функции распределения")
        self.ax.grid(True)
        n = int(self.n_value.get())
        p = float(self.probability_value.get())
        solution = Solution(p, n)
        series = solution.first_task()
        E, average, sigma, delta_average, var, S_2, delta_var, Me, R = solution.second_task()

        heads = ["y_i", "n_i", "n_i / n"]
        self.table = ttk.Treeview(self.master, show='headings', columns=heads, height=10)
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', width=150)
        for y_i, n_i in series:
            self.table.insert("", END, values=(y_i, n_i, n_i / n))
        self.scrollbary = Scrollbar(self.master, orient=VERTICAL)
        self.table.configure(yscrollcommand=self.scrollbary.set)
        self.scrollbary.configure(command=self.table.yview)

        topics = ["Mn", "x̂", "σ", "|Mn - x̂|", "Dn", "S^2", "|Dn - S^2|", "Me", "R"]
        self.table_characters = ttk.Treeview(self.master, show='headings', columns=topics, height=2)
        for topic in topics:
            self.table_characters.heading(topic, text=topic, anchor='center')
            self.table_characters.column(topic, anchor='center', width=150)
        self.table_characters.insert("", END, values=(E, average, sigma, delta_average, var, S_2, delta_var, Me, R))

        self.scrollbary.place(x=0, y=120, width=15, height=220)
        self.table.place(x=0, y=120)
        self.table_characters.place(x=460, y=120)

        parts = ['y_j', 'P(n = y_j)', 'n_j / n']
        self.probs_table = ttk.Treeview(self.master, show='headings', columns=parts, height=8)
        for part in parts:
            self.probs_table.heading(part, text=part, anchor='center')
            self.probs_table.column(part, anchor='center', width=150)
        max_deviation = 0
        for x_i, n_i in solution.series:
            self.probs_table.insert("", END, values=(x_i, solution.p * solution.q**(x_i - 1), n_i / solution.n))
            if math.fabs(n_i / solution.n - solution.p * solution.q**(x_i - 1)) > max_deviation:
                max_deviation = math.fabs(n_i / solution.n - solution.p * solution.q**(x_i - 1))

        self.scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.probs_table.yview)
        self.probs_table.place(x=0, y=370)
        self.scrollbar.place(x=0, y=370, height=180)

        solution.generate_data_for_plot()

        self.ax.plot((-2, 1), (0, 0), color='red', linewidth=2)
        self.ax.plot((-2, 1), (0, 0), color='blue', linewidth=2)
        for i in range(len(solution.series) - 1):
            self.ax.plot((solution.series[i][0], solution.series[i + 1][0]), (solution.prefix_sums[i],
                          solution.prefix_sums[i]), color='blue', linewidth=2)

        for i in range(1, 30):
            self.ax.plot((i, i + 1), (solution.sums[i - 1], solution.sums[i - 1]), color='red', linewidth=2)
        self.ax.plot((solution.series[-1][0], solution.series[-1][0] + 32), (1, 1), color='blue', linewidth=2, label='F^(x)')

        self.ax.plot((-3, 1), (0, 0), color='red', linewidth=2, label='F(x)')
        if solution.series[-1][0] > 30:
            self.ax.plot((31, solution.series[-1][0] + 2), (1, 1))

        self.ax.grid(True)
        self.ax.legend()
        chart = FigureCanvasTkAgg(self.fig, self.master)
        NavigationToolbar2Tk(chart).place(x=1320, y=950)
        chart.get_tk_widget().place(x=460, y=190)

        label = Label(self.master, text=f"Величина D = {solution.diff}", font="Consolas 12", background="#7FFFD4")
        max_deviation_label = Label(self.master, text=f"Величина max|n_j / n - P(n = y_j)| = {max_deviation}",
                                    font="Consolas 11", background="#7FFFD4")
        label.place(x=0, y=570)
        max_deviation_label.place(x=0, y=600)


ROOT = Tk()
gui = GUI(ROOT)
ROOT.mainloop()
