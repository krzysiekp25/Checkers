import tkinter as tk
from tkinter import messagebox

class View(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        super().__init__(self.root)
        self.__controller = None
        self.buttons = None
        self.clicked_button = None
        self.round = None
        self.__pionekb = tk.PhotoImage(file="img/pionekb.gif")
        self.__pionekbD = tk.PhotoImage(file="img/pionekbD.gif")
        self.__pionekbs = tk.PhotoImage(file="img/pionekbs.gif")
        self.__pionekbDs = tk.PhotoImage(file="img/pionekbDs.gif")
        self.__pionekc = tk.PhotoImage(file="img/pionekc.gif")
        self.__pionekcD = tk.PhotoImage(file="img/pionekcD.gif")
        self.__pionekcs = tk.PhotoImage(file="img/pionekcs.gif")
        self.__pionekcDs = tk.PhotoImage(file="img/pionekcDs.gif")
        self.__polec = tk.PhotoImage(file="img/polec.gif")
        self.__poleb = tk.PhotoImage(file="img/poleb.gif")

    def add_controller(self, controller):
        self.__controller = controller

    def clicked(self, r, c):
        self.__controller.clicked(r, c)

    def draw_board(self, board, n):
        self.pack()
        self.create_widgets(board, n)

    def draw_window(self, width=780, height=530, title='Warcaby'):
        self.root.geometry('{}x{}'.format(width, height))
        self.winfo_toplevel().title(title)

    def create_widgets(self, board, n):
        self.buttons = [[0 for _ in range(n)] for _ in range(n)]
        for x in range(0, n, 1):
            for y in range(0, n, 1):
                tmp = board[x][y]
                img = self.select_img(tmp.text)
                self.buttons[x][y] = tk.Button(self, text=tmp.text,
                                               command=lambda row=tmp.row, column=tmp.column: self.clicked(row, column),
                                               bg=tmp.bg, fg=tmp.fg, image=img, compound='none')
                buf = self.buttons[x][y]
                buf.grid(row=tmp.row, column=tmp.column)
        self.quit = tk.Button(self, text="ZAMKNIJ", fg="black", command=self.root.destroy, font=(None, 10))
        self.quit.grid(row=2, column=8)
        self.round = tk.Label(self, text="Tura gracza 1", fg="black", height=1, width=15, font=(None, 20))
        self.round.grid(row=0, column=8)

    def start_loop(self):
        self.mainloop()

    def update_button(self, tmp):
        img = self.select_img(tmp.text)
        self.buttons[tmp.row][tmp.column].destroy()
        self.buttons[tmp.row][tmp.column] = tk.Button(self, text=tmp.text,
                                                    command=lambda row=tmp.row, column=tmp.column: self.clicked(row,
                                                    column), bg=tmp.bg, fg=tmp.fg,
                                                      image=img, compound='none')
        buf = self.buttons[tmp.row][tmp.column]
        buf.grid(row=tmp.row, column=tmp.column)
        buf.update()

    def show_message(self, message):
        messagebox.showinfo("Uwaga", message)

    def change_round(self):
        if self.round['text'] == 'Tura gracza 1':
            self.round.config(text='Tura gracza 2')
        else:
            self.round.config(text='Tura gracza 1')

    def select_img(self, txt):
        if txt == 'b':
            return self.__polec
        if txt == 'w':
            return self.__poleb
        if txt == 'Pb':
            return self.__pionekb
        if txt == 'Pc':
            return self.__pionekc
        if txt == '[Pb]':
            return self.__pionekbs
        if txt == '[Pc]':
            return self.__pionekcs
        if txt == 'PbD':
            return self.__pionekbD
        if txt == 'PcD':
            return self.__pionekcD
        if txt == '[PbD]':
            return self.__pionekbDs
        if txt == '[PcD]':
            return self.__pionekcDs
