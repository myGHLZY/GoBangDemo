from Base import GameStatus

# 定义一个仿真次数
ROLLOUT_NUM = 200

class Node:
    def __init__(self, visited_num=0, parent=None, children=None, status=None):


        self.parent = parent
        self.children = children


        #探索次数
        self.visited_num = visited_num
        #是否为叶节点
        self.isLeaf = True
        # 游戏状态
        self.status = status
        #
        self.quality_value = 0.0


def best_chilrend(node):

    print()

# MCTS的选择
def selection(node):
    current_node = node
    # 当前节点不为叶节点的时候，找到最好的孩子叶节点。否则，返回当前节点
    while current_node.isLeaf == False:
        current_node = best_chilrend(current_node)
    return current_node

# 对每个传入的节点进行仿真，返回的是此节点的棋手在接下来胜的局数
def rollout(node):
    print()
    print()
    print()



