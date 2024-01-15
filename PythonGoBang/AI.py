from Base import Pieces,Player,Point,GameStatus,Board,Move
import random

class AI:
    def __init__(self,gameStatus):
        # print("实例化")
        self.gameStatus=gameStatus

    def moveStrategy(self):
        # self.gameStatus.show()

        point = self.gameStatus.board.randomMove()

        return point



