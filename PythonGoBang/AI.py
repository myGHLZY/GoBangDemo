from Base import Pieces,Player,Point,GameStatus,Board,Move
import random

class AI:
    def __init__(self,gameStatus):
        # print("实例化")
        self.gameStatus=gameStatus

    def moveStrategy(self):
        # self.gameStatus.show()

        point = self.gameStatus.board.randomMove()
        self.gameStatus.setMove(Move(point))

        return point

        # for i in range(0,self.gameStatus.board.rows):
        #     for j in range(0, self.gameStatus.board.cols):
        #         point = Point(i,j)
        #         if self.gameStatus.board.isLegalMove(point):
        #             self.gameStatus.setMove(Move(point))
        #             return point



