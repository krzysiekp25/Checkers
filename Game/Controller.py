class Controller:
    def __init__(self, view, model):
        self.__view = view
        self.__model = model

    def start(self):
        board = self.__model.create_board()
        n = self.__model.n
        self.__view.draw_window()
        self.__view.draw_board(board, n)
        self.__view.start_loop()

    def clicked(self, r, c):
        self.__model.select_button(r, c)

    def update_button(self, pionek):
        self.__view.update_button(pionek)

    def message(self, m):
        self.__view.show_message(m)


