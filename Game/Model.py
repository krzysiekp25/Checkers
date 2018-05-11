from Game.Pionek import *


class Model:
    def __init__(self):
        self.__board = None
        self.__n = 8
        self.__controller = None
        self.__selected_button = None
        self.__player_round = 1
        self.__player1_pionki = 12
        self.__player2_pionki = 12
        self.__reset = False

    def get_n(self):
        return self.__n

    def add_controller(self, controller):
        self.__controller = controller

    def create_board(self):
        self.__board = [["bc"[(i + j + self.__n % 2 + 1) % 2] for i in range(self.__n)] for j in range(self.__n)]
        for x in range(0, self.__n, 1):
            for y in range(0, self.__n, 1):
                if x in range(0, 3, 1) and self.__board[x][y] == 'c':
                    self.__board[x][y] = ZwyklyPionek(text='Pb', bg='black', fg='white', row=x, column=y, player=1)
                    #self.board[x][y] = Damka(text='PbD', bg='black', fg='white', row=x, column=y, player=1)
                elif x in range(5, 8, 1) and self.__board[x][y] == 'c':
                    self.__board[x][y] = ZwyklyPionek(text='Pc', bg='black', fg='white', row=x, column=y, player=2)
                elif self.__board[x][y] == 'c':
                    self.__board[x][y] = PustePole(text='b', bg='black', row=x, column=y)
                else:
                    self.__board[x][y] = PustePole(text='w', bg='white', row=x, column=y)
        return self.__board

    def select_button(self, r, c):
        clicked = self.__board[r][c]
        if self.__selected_button is not None and self.__selected_button.row == r and self.__selected_button.column == c:  # odznaczamy
            self.unselect_button()
        elif self.__selected_button is not None:  # zaznaczamy drugie pole
            if Pionek.have_beating(self.__player_round) is False and self.__selected_button.can_move(clicked, self.__board):
                self.move_button(self.__selected_button, clicked)
            elif self.__selected_button.beating() is True:
                if self.__selected_button.can_beat(clicked, self.__board):
                    self.beat_and_move(self.__selected_button, clicked)
                else:
                    self.__controller.message('Ruch niedozwolony!')
            else:
                self.__controller.message('Ruch niedozwolony!')
        elif type(clicked) is not PustePole and clicked.player is self.__player_round:  # zaznaczamy
            self.select(clicked)
        elif type(clicked) is not PustePole:
            self.__controller.message('Runda przeciwnika!')
        else:
            self.__controller.message('Nie mozna zaznaczyc pustego pola!')

    def select(self, pionek):
        self.__selected_button = pionek
        pionek.text = '[{}]'.format(pionek.text)
        self.__controller.update_button(pionek)

    def unselect_button(self):
        self.__selected_button.text = self.__selected_button.text[1:-1]
        self.__controller.update_button(self.__selected_button)
        self.__selected_button = None

    def move_button(self, pionek, pole):
        self.switch_places(pole, pionek)
        # if pionek jest na ostatnim polu, to zamien w damke
        self.unselect_button()
        self.switch_to_damka(pionek)
        self.change_round()

    def change_round(self):
        Pionek.have_beating1 = False
        Pionek.have_beating2 = False
        self.change_beating()  # ustawiamy beating player od nowa
        # nie zmieniamy kiedy mamy kolejne bicie
        if self.__player_round is 1:
            self.__player_round = 2
        else:
            self.__player_round = 1
        self.__controller.change_round()

    def change_beating(self):
        for x in self.__board:
            for y in x:
                if type(y) is not PustePole:
                    y.find_and_set_beating(self.__board, self.__n)

    def switch_places(self, first, second):

        # zapaietuje pozycje
        frow = first.row
        fcolumn = first.column
        srow = second.row
        scolumn = second.column

        # zamieniam pozycje w elementach
        second.row = frow
        second.column = fcolumn
        first.row = srow
        first.column = scolumn

        # zamieniam pozycje w tablicy
        tmp = first
        self.__board[frow][fcolumn] = self.__board[srow][scolumn]
        self.__board[srow][scolumn] = tmp

        # aktualizacja grafiki
        self.__controller.update_button(first)
        self.__controller.update_button(second)

    def beat_and_move(self, first, second):
        self.unselect_button()
        if type(first) is ZwyklyPionek:
            r = int((first.row + second.row) / 2)
            c = int((first.column + second.column) / 2)
            p = PustePole(text="b", bg="black", fg="white", row=r, column=c)
            self.__board[r][c] = p
            self.__controller.update_button(p)
        elif type(first) is Damka:
            r = int(first.row - second.row)
            c = int(first.column - second.column)
            p = None
            if r > 0 and c > 0:
                # gora lewo
                tmprow = first.row - 1
                tmpcolumn = first.column - 1
                while tmprow != second.row and tmpcolumn != second.column:
                    if type(self.__board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.__board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow - 1
                    tmpcolumn = tmpcolumn - 1
            elif r > 0 and c < 0:
                # gora prawo
                tmprow = first.row - 1
                tmpcolumn = first.column + 1
                while tmprow != second.row and tmpcolumn != second.column:
                    if type(self.__board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.__board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow - 1
                    tmpcolumn = tmpcolumn + 1
            elif r < 0 and c > 0:
                # dol lewo
                tmprow = first.row + 1
                tmpcolumn = first.column - 1
                while tmprow != second.row and tmpcolumn != second.column:
                    if type(self.__board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.__board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow + 1
                    tmpcolumn = tmpcolumn - 1
            elif r < 0 and c < 0:
                # dol prawo
                tmprow = first.row + 1
                tmpcolumn = first.column + 1
                while tmprow != second.row and tmpcolumn != second.column:
                    if type(self.__board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.__board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow + 1
                    tmpcolumn = tmpcolumn + 1
            p = PustePole(text="b", bg="black", fg="white", row=p.row, column=p.column)
            self.__board[p.row][p.column] = p
            self.__controller.update_button(p)
        self.switch_places(first, second)
        if self.__player_round is 1:
            self.__player2_pionki -= 1
        else:
            self.__player1_pionki -= 1
        if self.__player1_pionki is 0:
            self.__controller.message("Wygral gracz 2")
            self.reset_game()
        if self.__player2_pionki is 0:
            self.__controller.message("Wygral gracz 1")
            self.reset_game()

        # if runda bedzie sie zmieniac - czyli nie ma juz bicia
        if self.multiple_beating(first) is False:
            if self.__reset is False:
                self.switch_to_damka(first)
                self.change_round()
        else:
            self.select(first)
        self.__reset = False




    def switch_to_damka(self, pionek):
        if self.__player_round is 1:
            if pionek.row is self.__n - 1:
                d = Damka(text="PbD", row=pionek.row, column=pionek.column,
                                                              player=1)
                self.__board[pionek.row][pionek.column] = d
                self.__controller.update_button(d)
        elif self.__player_round is 2:
            if pionek.row is 0:
                d = Damka(text="PcD", row=pionek.row, column=pionek.column,
                                                              player=2)
                self.__board[pionek.row][pionek.column] = d
                self.__controller.update_button(d)

    def multiple_beating(self, first):
        first.find_and_set_beating(self.__board, self.__n)
        if first.beating() is True:
            return True
        else:
            return False

    def create_testing_board(self, number):
        self.__board = [["bc"[(i + j + self.__n % 2 + 1) % 2] for i in range(self.__n)] for j in range(self.__n)]
        for x in range(0, self.__n, 1):
            for y in range(0, self.__n, 1):
                if self.__board[x][y] == 'c':
                    self.__board[x][y] = PustePole(text='b', bg='black', row=x, column=y)
                else:
                    self.__board[x][y] = PustePole(text='w', bg='white', row=x, column=y)
        if number == 4:
            self.__board[1][1] = ZwyklyPionek(text='Pb', bg='black', fg='white', row=1, column=1, player=1)
            self.__board[1][1].set_beating()
            self.__board[2][2] = ZwyklyPionek(text='Pc', bg='black', fg='black', row=2, column=2, player=2)
            self.__board[2][2].unset_beating()
            self.__board[4][4] = ZwyklyPionek(text='Pc', bg='black', fg='black', row=4, column=4, player=2)
            self.__board[4][4].unset_beating()
            self.__board[4][6] = ZwyklyPionek(text='Pc', bg='black', fg='black', row=4, column=6, player=2)
            self.__board[4][6].unset_beating()
            Pionek.have_beating1 = True
            Pionek.have_beating2 = False
            self.__player_round = 1
            self.__player1_pionki = 1
            self.__player2_pionki = 3
        if number == 5:
            self.__board[1][1] = ZwyklyPionek(text='Pc', bg='black', fg='black', row=1, column=1, player=2)
            self.__board[1][1].unset_beating()
            self.__board[1][5] = ZwyklyPionek(text='Pb', bg='black', fg='black', row=1, column=5, player=1)
            self.__board[1][5].unset_beating()
            Pionek.have_beating1 = False
            Pionek.have_beating2 = False
            self.__player_round = 2
            self.__player1_pionki = 1
            self.__player2_pionki = 1
        self.__controller.create_testing_board(self.__board)
        if self.__player_round == 2:
            self.__controller.change_round()
        # po kliknieciu na przyciski z prawej strony które MUSZE GENEROWAC TUTAJ A NIE W VIEW
        # powinno uruchomik odpowiednią planszę testową o odpowiednim numerze :P
        # controler wysyla informacje o kliknieciu, ustawiamy zmienne modelu tworzymy odpowiedni board i wysylamy do funkcji
        # create_testing_board

    def reset_game(self):
        if self.__selected_button is not None:
            self.__selected_button = None
        self.__player_round = 1
        self.__player1_pionki = 12
        self.__player2_pionki = 12
        self.__controller.reset()
        self.__reset = True
        Pionek.have_beating1 = False
        Pionek.have_beating2 = False

    def hard_reset(self):
        if self.__selected_button is not None:
            self.__selected_button = None
        self.__player_round = 1
        self.__player1_pionki = 12
        self.__player2_pionki = 12
        Pionek.have_beating1 = False
        Pionek.have_beating2 = False