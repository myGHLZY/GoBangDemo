from AI import AI
from Base import Pieces,Player,Point,GameStatus,Board


def test():
    # 创建一个棋盘
    board = Board(10, 8)
    # 创建游戏状态类
    gameStatus = GameStatus(board, player=Player.BLACK, move=None)

    gameStatus.randomMoveMCTS(1)


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
        # print(point)
        status = AI1.gameStatus.applyMove(point,Player.BLACK)
        if status == "OVER":
            break
        AI1.gameStatus.player = AI1.gameStatus.player.other
        point = AI2.moveStrategy()
        status = AI2.gameStatus.applyMove(point, Player.WHITE)
        if status == "OVER":
            break
        AI1.gameStatus.player = AI1.gameStatus.player.other



if __name__ == '__main__':
    start()
    # test()