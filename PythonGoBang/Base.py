import collections
import random
import copy
import numpy as np
from enum import Enum
import enum
import time

'''
    表示我们下的是几子棋
'''
NUM_WIN = 5

'''
    命名元组
    
'''

Point = collections.namedtuple("Point",["row","col"])

'''
棋子颜色类
'''

class Pieces(Enum):
    EMPTY = 0
    BLACK = -1
    WHITE = 1

'''
    棋盘点类  我们已经替换为命名元组  
'''
# class Point:
#     def __init__(self, row, col):
#         self.row = row
#         self.col = col
#
#     def getPoint(self):
#         print("("+str(self.row)+","+str(self.col)+")")




'''
    棋盘类 我们用 0代表空 1代表白 -1代表黑
    
    用一个二维列表表示棋盘
    
    棋盘有一个成员变量 move 代表此局游戏执棋方的落子
    
'''


class Board:

    def __init__(self, rows, columns):
        self.rows = rows     #假如是3行的话，我们的行数是 0 1 2
        self.cols = columns
        # TODO ‘是否考虑将二维列表变为一个字典’(二维列表比字典容易判断胜负！两者都可有)
        self._grid = [[0 for _ in range(columns)] for _ in range(rows)]
        self.move = None

        # 记录所有的合法走子方法，为了方便删、查，用字典存储
        self.legalMove= self.initLegalMove()


    '''
        Board类的一些方法
    '''

    def reset(self):
        self._grid = [[0 for _ in range(len(sublist))] for sublist in self._grid]
        self.legalMove = self.initLegalMove()

    def initLegalMove(self):
        dic = {}
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                # 由于不可变类、与可变类存在 这里不能用Point类 考虑用元组
                dic[Point(i,j)] = 0
        return dic

    def getEmptyPointNum(self):
        return len(self.legalMove)

    def randomMove(self):

        # point = random.sample(self.legalMove.keys(), 1)
        point = random.choice(list(self.legalMove.keys()))

        return point


    def getGrid(self):
        return self._grid

    def isFull(self):
        arr = np.array(self._grid)
        # 全不为0(满) 返回True
        if np.all(arr != 0 ):
            return True
        return False

    def isEmpty(self):
        arr = np.array(self._grid)
        if np.all(arr == 0):
            return True
        return False

    #判断棋子是否在棋盘上
    def onBoard(self, point):
        return point.row <= self.rows-1 and point.col <= self.cols-1

    def getBoardRows(self):
        return self.rows

    def getBoardCols(self):
        return self.cols

    #落子的地方为空
    def emptyPoint(self,point):
        return self._grid[point.row][point.col] == 0

    # 棋盘不空且落子合法
    def isLegalMove(self, point):
        return not self.isFull() and self.onBoard(point) and self.emptyPoint(point)

    def applyMove(self, point, player):
        self._grid[point.row][point.col] = player.value
        del self.legalMove[point]
        # print(len(self.legalMove))

    def show(self):
        print("   ",end="")
        for j in range(0,len(self._grid[0])):
            print(j,end="  ")
        print()
        for i in range(0, len(self._grid)):
            print(i, end="  ")
            for j in range(0,len(self._grid[0])):
                if self._grid[i][j] == 0:
                    print("*",end="  ")
                elif self._grid[i][j] == 1:
                    print("\033[34mo\033[0m",end="  ")
                elif self._grid[i][j] == -1:
                    print("\033[31mx\033[0m",end="  ")
            print()



'''
棋手类

'''


class Player(enum.Enum):
    BLACK = -1
    WHITE = 1

    @property
    def other(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE

    # @property
    # def self(self):
    #     return Player.WHITE if self == Player.WHITE else Player.WHITE

'''
落子类
    落子类主要是有三种落子的策略：正常落子/pass/认输

'''


class Move:
    def __init__(self, point, is_pass=False, is_resign=False):
        # print("获得的point",point)
        # assert True 正常运行
        # assert (point is None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign


    # @classmethod
    def getPointDiscription(self):
        print("("+str(self.point.row)+","+str(self.point.col)+")")

    def getPoint(self):
        return self.point



'''
游戏状态类，我们上述的所有类都会在此类中用到
'''


class GameStatus:
    '''
    :param 棋盘 当前的执棋方 落子
    '''
    def __init__(self,board, player, move):
        self.board = board
        self.player = player
        self.move = move

    def reset(self):
        self.board.reset()
        self.move = None
        self.player = Player.BLACK

    #专用于蒙特卡罗的随机下法
    def randomMoveMCTS(self,rollout_num):
        #当前方从此节点进行模拟，胜利的局数
        num_win = 0
        # 复制一份游戏状态
        # 额外复制一份randomMove
        gameStatus = copy.copy(self)
        start_player = gameStatus.player
        start = time.time()
        for i in range(0,rollout_num):
            while True:
                status = self.applyMove(self.board.randomMove(), start_player)
                if status == "OVER":
                    num_win+=1
                    break
                gameStatus.player = gameStatus.player.other
                status = self.applyMove(self.board.randomMove(), start_player.other)
                if status == "OVER":
                    break
                gameStatus.player = gameStatus.player.other
            gameStatus.reset()
        end = time.time()
        print("***此次模拟结束***")
        print("模拟开始方是",str(start_player)," 胜局",str(num_win),"\n总模拟局数",str(rollout_num))
        print("胜率是："+str(num_win)+"/"+str(rollout_num)+" = ",num_win/rollout_num)
        print("总耗时：",end - start)
        return num_win


    '''
    我们将判断游戏是否结束的逻辑放在GameStatus中
    '''

    # 以棋盘的左上角为原点，向下，向右为正方向
    def isWin(self):
        y = self.move.getPoint().row
        x = self.move.getPoint().col

        # 判断一行是否有NUM_WIN个棋子属于当前颜色
        num_wim = 0
        for i in range(0,self.board.getBoardCols()):
            if self.board.getGrid()[y][i] == self.player.value:
                num_wim+=1
                if num_wim>=NUM_WIN:
                    return True
            else:
                num_wim=0
        # 一列
        num_wim = 0
        for i in range(0,self.board.getBoardRows()):
            if self.board.getGrid()[i][x] == self.player.value:
                num_wim += 1
                if num_wim >= NUM_WIN:
                    return True
            else:
                num_wim=0


        # 斜率小于0的斜线(考虑棋盘不是一个正方形)
        num_wim = 0
        if x >= y:
            i = 0
            j = x - y
        else:
            i = y - x
            j = 0
        while i < self.board.getBoardCols() and j < self.board.getBoardRows():
            if self.board.getGrid()[i][j] == self.player.value:
                num_wim += 1
                if num_wim >= NUM_WIN:
                    return True
            else:
                num_wim = 0
            i += 1
            j += 1

        # 斜率大于0的斜线
        num_wim = 0
        if y <= self.board.getBoardCols() - 1 - x:
            i = 0
            j = x + y
        else:
            i = y + x - self.board.getBoardCols() + 1
            j = self.board.getBoardCols() - 1
        while i < self.board.getBoardCols() and j < self.board.getBoardRows():
            if self.board.getGrid()[i][j] == self.player.value:
                num_wim += 1
                if num_wim >= NUM_WIN:
                    return True
            else:
                num_wim = 0
            i -= 1
            j += 1

        return False

    #平局在胜局的基础上判断，所以，子满了就是平局
    def isTie(self):
        return self.board.getEmptyPointNum() == 0

    def setMove(self,move):
        self.move = move


    # 游戏是否结束
    # TODO 平局的逻辑也要加上
    def isOver(self):
        if self.isWin():
            return "WIN"
        if self.isTie():
            return "TIE"




    # 走子
    def applyMove(self, point, player):
        self.setMove(Move(point))
        self.board.applyMove(point,player)
        self.show()
        if self.isOver() != None:
            print('========')
            print("游戏结束")
            if self.isOver() == "WIN":
                print("*****   "+str(player) + "获胜")
            elif self.isOver() == "TIE":
                print("*****   平局   *****")
            print('========')
            return "OVER"

    #打印方法
    def show(self):
        print("\n\n=======打印游戏状态========\n")
        self.board.show()

        if self.move is not None:
            print(str(self.player)+"落子  "+"刚才落子的位置是：",end="")
            self.move.getPointDiscription()

    def isLegel(self,point):
        self.board.isLigelMove(point)











