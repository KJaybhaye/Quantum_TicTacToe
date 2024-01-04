import numpy as np
import pickle
import copy
from symb import Symb

class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = [] 
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}
    
    def entangled(self, board):
        en = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j].entangled:
                    en.append([i,j,board[i][j].entangled.pos])
        if en:
            return en
        return [0]

    def getHash(self, board):
        boardHash = str([[board[i][j].pos, board[i][j].val, board[i][j].empty] for j in range(len(board)) for i in range(len(board[0]))]+self.entangled(board))
        return boardHash
    
    def updateBoard(self, board, position, act='m'):
        if act == 'e':
          board[position[0][0]][position[0][1]].entangle(board[position[1][0]][position[1][1]])
          return board
        if act == 'p':
          board[position[0]][position[1]] = Symb(pos=[position[0],position[1]])
          return board
        board[position[0]][position[1]].measure()
        return board

    def chooseAction(self, combs, current_board):
        if np.random.uniform(0, 1) <= self.exp_rate:
            ind = np.random.choice(len(combs))
            action, pos = combs[ind]
            return action, pos
        else:
            value_max = -999
            for a, p in combs:
                next_board = copy.deepcopy(current_board)
                next_board = self.updateBoard(next_board, p, a)
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action, pos = a, p
            return action, pos

    def addState(self, state):
        self.states.append(state)

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr*(self.decay_gamma*reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self, num=0):
        fw = open('./Policies/policy_' + str(self.name) + f'_{num}', 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file,'rb')
        self.states_value = pickle.load(fr)
        fr.close()
