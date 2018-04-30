class Pionek():
    def __init__(self, text="Pb", bg="black", fg="white", row=0, column=0, height=4, width=8):
        self.text = text
        self.row = row
        self.column = column
        self.bg = bg
        self.fg = fg
        self.height = height
        self.width = width

class ZwyklyPionek(Pionek):
    def __init__(self, text="Pb", bg="black", fg="white", row=0, column=0, height=4, width=8, player=1):
        super().__init__(text, bg, fg, row, column, height, width)
        self.player = player

class Damka(Pionek):
    def __init__(self, text="Pb", bg="black", fg="white", row=0, column=0, height=4, width=8, player=1):
        super().__init__(text, bg, fg, row, column, height, width)
        self.player = player

class PustePole(Pionek):
    def __init__(self, text="Pb", bg="black", fg="white", row=0, column=0, height=4, width=8):
        super().__init__(text, bg, fg, row, column, height, width)
