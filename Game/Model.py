from Game.Pionek import *

class Model:
    def __init__(self):
        self.__controller = None
        self.board = None
        self.n = 8
        self.selected_button = None
        self.player_round = 1
        self.beating_player_1 = False
        self.beating_player_2 = False

    def add_controller(self, controller):
        self.__controller = controller

    def create_board(self):
        self.board = [["bc"[(i + j + self.n % 2 + 1) % 2] for i in range(self.n)] for j in range(self.n)]
        for x in range(0, self.n, 1):
            for y in range(0, self.n, 1):
                if x in range(0, 3, 1) and self.board[x][y] == 'c':
                    self.board[x][y] = ZwyklyPionek(text='Pb', bg='black', fg='white', row=x, column=y, player=1)
                elif x in range(5, 8, 1) and self.board[x][y] == 'c':
                    self.board[x][y] = ZwyklyPionek(text='Pc', bg='black', fg='white', row=x, column=y, player=2)
                elif self.board[x][y] == 'c':
                    self.board[x][y] = PustePole(text='', bg='black', row=x, column=y)
                else:
                    self.board[x][y] = PustePole(text='', bg='white', row=x, column=y)
        return self.board

    def select_button(self, r, c):
        clicked = self.board[r][c]
        if self.selected_button is not None and self.selected_button.row == r and self.selected_button.column == c:#odznaczamy
            self.unselect_button()
        elif self.selected_button is not None:#zaznaczamy drugie pole
            if self.beating_player_1 is True and self.player_round is 2 and self.selected_button.can_move(clicked, self.board, self.player_round):
                self.move_button(self.selected_button, clicked)
            elif self.beating_player_2 is True and self.player_round is 1 and self.selected_button.can_move(clicked, self.board, self.player_round):
                self.move_button(self.selected_button, clicked)
            elif self.beating_player_1 is False and self.beating_player_2 is False and self.selected_button.can_move(clicked, self.board, self.player_round):
                self.move_button(self.selected_button, clicked)
            elif self.beating_player_1 is True and self.player_round is 1:
                if self.selected_button.can_beat(clicked, self.board):
                    self.beat_and_move(self.selected_button, clicked)
                    self.__controller.message('Bicie!')
                else:
                    self.__controller.message('Ruch niedozwolony!')
            elif self.beating_player_2 is True and self.player_round is 2:
                if self.selected_button.can_beat(clicked, self.board):
                    self.beat_and_move(self.selected_button, clicked)
                    self.__controller.message('Bicie!')
                else:
                    self.__controller.message('Ruch niedozwolony!')
            else:
                self.__controller.message('Ruch niedozwolony!')
        elif type(clicked) is not PustePole and clicked.player is self.player_round:#zaznaczamy
            self.select(clicked)
        elif type(clicked) is not PustePole:
            self.__controller.message('Runda przeciwnika!')
        else:
            self.__controller.message('Nie mozna zaznaczyc pustego pola!')

    def select(self, pionek):
        self.selected_button = pionek
        pionek.text = '[{}]'.format(pionek.text)
        self.__controller.update_button(pionek)

    def unselect_button(self):
        self.selected_button.text = self.selected_button.text[1:-1]
        self.__controller.update_button(self.selected_button)
        self.selected_button = None

    def move_button(self, pionek, pole):
        self.unselect_button()
        self.switch_places(pole, pionek)
        self.change_round()

    def change_round(self):
        aktualneb1 = self.beating_player_1
        aktualneb2 = self.beating_player_2
        if aktualneb1 is True and self.player_round is 2:
            aktualneb1 = False
        if aktualneb2 is True and self.player_round is 1:
            aktualneb2 = False
        self.change_beating()#ustawiamy beating player od nowa
        #nie zmieniamy kiedy mamy kolejne bicie
        if aktualneb1 is True and self.beating_player_1 is True:
            pass
        elif aktualneb2 is True and self.beating_player_2 is True:
            pass
        else:
            if self.player_round is 1:
                self.player_round = 2
            else:
                self.player_round = 1
        #dodac rysowanie na planszy informacji czyja runda

    def change_beating(self):
        self.beating_player_1 = False
        self.beating_player_2 = False
        for x in self.board:
            for y in x:
                if type(y) is ZwyklyPionek:
                    r = y.row
                    c = y.column
                    if r+2 < self.n and c+2 < self.n:#prawo dół
                        if y.can_beat(self.board[r+2][c+2], self.board):
                            self.set_beating(y)
                    if r+2 < self.n and c-2 >= 0:#lewo dół
                        if y.can_beat(self.board[r+2][c-2], self.board):
                            self.set_beating(y)
                    if r-2 >= 0 and c+2 < self.n:#prawo góra
                        if y.can_beat(self.board[r-2][c+2], self.board):
                            self.set_beating(y)
                    if r-2 >= 0 and c-2 >= 0:#lewo góra
                        if y.can_beat(self.board[r-2][c-2], self.board):
                            self.set_beating(y)

    def switch_places(self, first, second):
        #zapaietuje pozycje
        frow = first.row
        fcolumn = first.column
        srow = second.row
        scolumn = second.column
        #zamieniam pozycje w elementach
        second.row = frow
        second.column = fcolumn
        first.row = srow
        first.column = scolumn
        #zamieniam pozycje w tablicy
        tmp = first
        self.board[frow][fcolumn] = self.board[srow][scolumn]
        self.board[srow][scolumn] = tmp
        #aktualizacja grafiki
        self.__controller.update_button(first)
        self.__controller.update_button(second)

    def set_beating(self, pionek):
        if pionek.player is 1:
            self.beating_player_1 = True
        elif pionek.player is 2:
            self.beating_player_2 = True

    def beat_and_move(self, first, second):
        self.unselect_button()
        if type(first) is ZwyklyPionek:
            r = int((first.row + second.row) / 2)
            c = int((first.column + second.column) / 2)
            p = PustePole(text="", bg="black", fg="white", row=r, column=c)
            self.board[r][c] = p
            self.__controller.update_button(p)
        self.switch_places(first, second)
        self.change_round()