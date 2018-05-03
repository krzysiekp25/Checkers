import tkinter as tk
from tkinter import messagebox

class View(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        super().__init__(self.root)
        self.__controller = None
        self.buttons = None
        self.clicked_button = None
        self.round = None
        self.pionekb = tk.PhotoImage(file="img/pionekb.gif")
        self.pionekbD = tk.PhotoImage(file="img/pionekbD.gif")
        self.pionekbs = tk.PhotoImage(file="img/pionekbs.gif")
        self.pionekbDs = tk.PhotoImage(file="img/pionekbDs.gif")
        self.pionekc = tk.PhotoImage(file="img/pionekc.gif")
        self.pionekcD = tk.PhotoImage(file="img/pionekcD.gif")
        self.pionekcs = tk.PhotoImage(file="img/pionekcs.gif")
        self.pionekcDs = tk.PhotoImage(file="img/pionekcDs.gif")
        self.polec = tk.PhotoImage(file="img/polec.gif")
        self.poleb = tk.PhotoImage(file="img/poleb.gif")

    def add_controller(self, controller):
        self.__controller = controller

    def clicked(self, r, c):
        self.__controller.clicked(r, c)

    def draw_board(self, board, n):
        self.pack()
        self.create_widgets(board, n)

    def draw_window(self, width=700, height=600, title='Warcaby'):
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
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.root.destroy)
        self.quit.grid(row=2, column=8)
        self.round = tk.Label(self, text="Tura gracza 1", fg="red", height=4, width=16)
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
            return self.polec
        if txt == 'w':
            return self.poleb
        if txt == 'Pb':
            return self.pionekb
        if txt == 'Pc':
            return self.pionekc
        if txt == '[Pb]':
            return self.pionekbs
        if txt == '[Pc]':
            return self.pionekcs
        if txt == 'PbD':
            return self.pionekbD
        if txt == 'PcD':
            return self.pionekcD
        if txt == '[PbD]':
            return self.pionekbDs
        if txt == '[PcD]':
            return self.pionekcDs
