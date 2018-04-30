from Game.Model import Model
from Game.View import View
from Game.Controller import Controller

class Application:
    def __init__(self):
        self.__view = View()
        self.__model = Model()
        self.__controller = Controller(self.__view, self.__model)
        self.__view.add_controller(self.__controller)
        self.__model.add_controller(self.__controller)

    def start(self):
        self.__controller.start()
