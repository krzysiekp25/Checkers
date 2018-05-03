from Game.Pionek import *


class Model:
    def __init__(self):
        self.__controller = None
        self.board = None
        self.n = 8
        self.selected_button = None
        self.player_round = 1

    def add_controller(self, controller):
        self.__controller = controller

    def create_board(self):
        self.board = [["bc"[(i + j + self.n % 2 + 1) % 2] for i in range(self.n)] for j in range(self.n)]
        for x in range(0, self.n, 1):
            for y in range(0, self.n, 1):
                if x in range(0, 3, 1) and self.board[x][y] == 'c':
                    self.board[x][y] = ZwyklyPionek(text='Pb', bg='black', fg='white', row=x, column=y, player=1)
                    #self.board[x][y] = Damka(text='Pbd', bg='black', fg='white', row=x, column=y, player=1)
                elif x in range(5, 8, 1) and self.board[x][y] == 'c':
                    self.board[x][y] = ZwyklyPionek(text='Pc', bg='black', fg='white', row=x, column=y, player=2)
                elif self.board[x][y] == 'c':
                    self.board[x][y] = PustePole(text='b', bg='black', row=x, column=y)
                else:
                    self.board[x][y] = PustePole(text='w', bg='white', row=x, column=y)
        return self.board

    def select_button(self, r, c):
        clicked = self.board[r][c]
        if self.selected_button is not None and self.selected_button.row == r and self.selected_button.column == c:  # odznaczamy
            self.unselect_button()
        elif self.selected_button is not None:  # zaznaczamy drugie pole
            if Pionek.have_beating(self.player_round) is False and self.selected_button.can_move(clicked, self.board):
                self.move_button(self.selected_button, clicked)
            elif self.selected_button.beating() is True:
                if self.selected_button.can_beat(clicked, self.board):
                    self.beat_and_move(self.selected_button, clicked)
                else:
                    self.__controller.message('Ruch niedozwolony!')
            else:
                self.__controller.message('Ruch niedozwolony!')
        elif type(clicked) is not PustePole and clicked.player is self.player_round:  # zaznaczamy
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
        if self.player_round is 1:
            self.player_round = 2
        else:
            self.player_round = 1
        self.__controller.change_round()

    def change_beating(self):
        for x in self.board:
            for y in x:
                if type(y) is not PustePole:
                    y.find_and_set_beating(self.board, self.n)

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
        self.board[frow][fcolumn] = self.board[srow][scolumn]
        self.board[srow][scolumn] = tmp

        # aktualizacja grafiki
        self.__controller.update_button(first)
        self.__controller.update_button(second)

    def beat_and_move(self, first, second):
        self.unselect_button()
        if type(first) is ZwyklyPionek:
            r = int((first.row + second.row) / 2)
            c = int((first.column + second.column) / 2)
            p = PustePole(text="b", bg="black", fg="white", row=r, column=c)
            self.board[r][c] = p
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
                    if type(self.board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow - 1
                    tmpcolumn = tmpcolumn - 1
            elif r > 0 and c < 0:
                # gora prawo
                tmprow = first.row - 1
                tmpcolumn = first.column + 1
                while tmprow != second.row and tmpcolumn != second.column:
                    if type(self.board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow - 1
                    tmpcolumn = tmpcolumn + 1
            elif r < 0 and c > 0:
                # dol lewo
                tmprow = first.row + 1
                tmpcolumn = first.column - 1
                while tmprow != second.row and tmpcolumn != second.column:
                    if type(self.board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow + 1
                    tmpcolumn = tmpcolumn - 1
            elif r < 0 and c < 0:
                # dol prawo
                tmprow = first.row + 1
                tmpcolumn = first.column + 1
                while tmprow != second.row and tmpcolumn != second.column:
                    if type(self.board[tmprow][tmpcolumn]) is not PustePole:
                        p = self.board[tmprow][tmpcolumn]
                        break
                    tmprow = tmprow + 1
                    tmpcolumn = tmpcolumn + 1
            p = PustePole(text="b", bg="black", fg="white", row=p.row, column=p.column)
            self.board[p.row][p.column] = p
            self.__controller.update_button(p)
        self.switch_places(first, second)
        # if runda bedzie sie zmieniac - czyli nie ma juz bicia
        if self.multiple_beating(first):
            self.switch_to_damka(first)
            self.change_round()




    def switch_to_damka(self, pionek):
        if self.player_round is 1:
            if pionek.row is self.n - 1:
                d = Damka(text="PbD", row=pionek.row, column=pionek.column,
                                                              player=1)
                self.board[pionek.row][pionek.column] = d
                self.__controller.update_button(d)
        elif self.player_round is 2:
            if pionek.row is 0:
                d = Damka(text="PcD", row=pionek.row, column=pionek.column,
                                                              player=2)
                self.board[pionek.row][pionek.column] = d
                self.__controller.update_button(d)

    def multiple_beating(self, first):
        # jako argument podac jeszcze stara pozycje i juz jej nie sprawdzac.
        # badamy otoczenie pionka i jesli znajdziemy bicie do pewnej pozycji to zwracamy prawde
        return True