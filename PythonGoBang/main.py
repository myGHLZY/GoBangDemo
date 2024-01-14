from AI import AI
from Base import Pieces,Player,Point,GameStatus,Board


def start():

    #创建一个棋盘
    board = Board(10,10)
    #创建游戏状态类
    gameStatus = GameStatus(board,player=Player.BLACK,move=None)

    #创建下棋的AI
    AI1 = AI(gameStatus)
    AI2 = AI(gameStatus=AI1.gameStatus)

    while True:
        point = AI1.moveStrategy()
        status = AI1.gameStatus.applyMove(point,Player.BLACK)
        if status == "OVER":
            break
        point = AI2.moveStrategy()
        status = AI2.gameStatus.applyMove(point, Player.WHITE)
        if status == "OVER":
            break



if __name__ == '__main__':
    start()