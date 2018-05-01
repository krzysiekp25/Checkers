from Game.Pionek import *

class Model:
    def __init__(self):
        self.__controller = None
        self.board = None
        self.n = 8
        self.selected_button = None
        self.player_round = 1
        self.beating = 0

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
            if self.selected_button.can_move(clicked, self.board, self.player_round):
                self.move_button(self.selected_button, clicked)
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
        # badamy całą planszę i to czy nie ma bicia, jak tak to ustawiamy flagę bicia
        if self.player_round is 1:
            self.player_round = 2
        else:
            self.player_round = 1
        #dodac rysowanie na planszy informacji czyja runda

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