import tkinter as tk
from tkinter import messagebox

class View(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        super().__init__(self.root)
        self.__controller = None
        self.buttons = None
        self.clicked_button = None

    def add_controller(self, controller):
        self.__controller = controller

    def clicked(self, r, c):
        self.__controller.clicked(r, c)

    def draw_board(self, board, n):
        self.pack()
        self.create_widgets(board, n)

    def draw_window(self, width=800, height=640, title='hejo'):
        self.root.geometry('{}x{}'.format(width, height))
        self.winfo_toplevel().title(title)

    def create_widgets(self, board, n):
        self.buttons = [[0 for _ in range(n)] for _ in range(n)]
        for x in range(0, n, 1):
            for y in range(0, n, 1):
                tmp = board[x][y]
                self.buttons[x][y] = tk.Button(self, text=tmp.text,
                                               command=lambda row=tmp.row, column=tmp.column: self.clicked(row, column),
                                               bg=tmp.bg, fg=tmp.fg, height=tmp.height, width=tmp.width)
                buf = self.buttons[x][y]
                buf.grid(row=tmp.row, column=tmp.column)
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.root.destroy)
        self.quit.grid(row=8, column=8)

    def start_loop(self):
        self.mainloop()

    def update_button(self, tmp):
        self.buttons[tmp.row][tmp.column].destroy()
        self.buttons[tmp.row][tmp.column] = tk.Button(self, text=tmp.text,
                                                    command=lambda row=tmp.row, column=tmp.column: self.clicked(row,
                                                    column), bg=tmp.bg, fg=tmp.fg, height=tmp.height, width=tmp.width)
        buf = self.buttons[tmp.row][tmp.column]
        buf.grid(row=tmp.row, column=tmp.column)

    def show_message(self, message):
        messagebox.showinfo("Uwaga", message)
