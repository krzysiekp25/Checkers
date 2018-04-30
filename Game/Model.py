from Game.Pionek import *

class Model:
    def __init__(self):
        self.__controller = None
        self.board = None
        self.n = 8
        self.selected_button = [None, None]
        self.player_round = 1

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
        if self.selected_button[0] == r and self.selected_button[1] == c:
            #jeżeli juz zaznaczony to odznaczamy i ustawiamy selected_button na none
            self.unselect_button(clicked)

        elif self.selected_button[0] is not None and self.selected_button[1] is not None:
            #jeeli jeden zaznaczony, to przy zaznaczeniu drugiego wykonujemy operacje
            selected = self.board[self.selected_button[0]][self.selected_button[1]]
            #self.__controller.message('Aktualnie zaznaczono pole {}{}. W tym czasie wybrałeś pole {}{}()'.format(self.selected_button[0], self.selected_button[1], r, c, self.player_round))
            if type(clicked) is PustePole and self.player_round is 1:
                if r - self.selected_button[0] is 1 and abs(self.selected_button[1] - c) is 1:
                    self.unselect_button(selected)
                    self.switch_places(clicked, selected)
                    self.change_round()

            elif type(clicked) is PustePole and self.player_round is 2:
                if self.selected_button[0] - r is 1 and abs(self.selected_button[1] - c) is 1:
                    self.unselect_button(selected)
                    self.switch_places(clicked, selected)
                    self.change_round()

        elif type(clicked) is not PustePole and clicked.player is self.player_round:
            #nic nie jest zaznaczone wiec zaznaczamy buttona w pozycji r, c
            clicked.text = '[{}]'.format(clicked.text)
            self.selected_button[0] = r
            self.selected_button[1] = c
            self.__controller.update_button(clicked)

    def unselect_button(self, pionek):
        pionek.text = pionek.text[1:-1]
        self.selected_button[0] = None
        self.selected_button[1] = None
        self.__controller.update_button(pionek)

    def change_round(self):
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