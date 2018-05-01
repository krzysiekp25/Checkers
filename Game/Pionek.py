class Pionek():
    def __init__(self, text="Pb", bg="black", fg="white", row=0, column=0, height=4, width=8):
        self.text = text
        self.row = row
        self.column = column
        self.bg = bg
        self.fg = fg
        self.height = height
        self.width = width

    def can_move(self, clicked, board, round):
        return None

    def can_beat(self, clicked, board, round):
        return None

class ZwyklyPionek(Pionek):
    def __init__(self, text="Pb", bg="black", fg="white", row=0, column=0, height=4, width=8, player=1):
        super().__init__(text, bg, fg, row, column, height, width)
        self.player = player

    def can_move(self, clicked, board, round):
        #srawdzamy czy nasz pionek moze sie ruszyc w dane klikniete miejsce badajac rundę
        if type(clicked) is PustePole:
            if round is 1:
                if clicked.row - self.row is 1 and abs(self.column - clicked.column) is 1:
                    return True
                else:
                    return False
            elif round is 2:
                if self.row - clicked.row is 1 and abs(self.column - clicked.column) is 1:
                    return True
                else:
                    return False
        else:
            return False

        def can_beat(self, clicked, board, round):
            return None

class Damka(Pionek):
    def __init__(self, text="Pb", bg="black", fg="white", row=0, column=0, height=4, width=8, player=1):
        super().__init__(text, bg, fg, row, column, height, width)
        self.player = player

class PustePole(Pionek):
    def __init__(self, text="", bg="black", fg="white", row=0, column=0, height=4, width=8):
        super().__init__(text, bg, fg, row, column, height, width)
