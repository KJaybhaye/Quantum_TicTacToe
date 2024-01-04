from symb import Symb
import random
from human import HumanPlayer


class State:
    def __init__(self, p1, p2, row=3, col=3):
        # self.board = np.full((self.row, self.col), 10)
        self.board = [[Symb(empty=True) for i in range(col)] for j in range(row)]
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        self.row = row 
        self.col = col
        self.playerSymbol = 1
        self.embsym = 2

    def getHash(self):
        self.boardHash = str([[self.board[i][j].pos, self.board[i][j].val, self.board[i][j].empty] for j in range(self.col) for i in range(self.row)]+self.entangled())
        return self.boardHash
    
    def entangled(self):
        en = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j].entangled:
                    en.append([i,j,self.board[i][j].entangled.pos])
                # en.append([i,j,self.board[i][j].pos])
        if en:
            return en
        return [0]

    def winner(self):
        for i in range(self.row):
            if sum([self.board[i][j].val for j in range(self.col)]) == 3:
                self.isEnd = True
                return 1
            if sum([self.board[i][j].val for j in range(self.col)]) == -3:
                self.isEnd = True
                return -1
            
        for i in range(self.col):
            if sum([self.board[j][i].val for j in range(self.row)]) == 3:
                self.isEnd = True
                return 1
            if sum([self.board[j][i].val for j in range(self.row)]) == -3:
                self.isEnd = True
                return -1
            
        diag_sum1 = sum([self.board[i][i].val for i in range(self.col)])
        diag_sum2 = sum([self.board[i][self.col-i-1].val for i in range(self.col)])

        if diag_sum1 == 3 or diag_sum2 == 3:
            self.isEnd = True
            return 1
        if diag_sum1 == -3 or diag_sum2 == -3:
            self.isEnd = True
            return -1

        if len(self.availablePositions()) == 0 and len(self.measured()) == self.col*self.row:
            self.isEnd = True
            return 0
        
        self.isEnd = False
        return None

    def availablePositions(self):
        positions = []
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j].empty:
                    positions.append([i, j])  # need to be tuple
        return positions

    def placed(self):
        positions = []
        for i in range(self.row):
            for j in range(self.col):
                if not self.board[i][j].empty:
                    positions.append([i, j])  # need to be tuple
        return positions
    
    def measured(self):
        positions = []
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j].val != 0:
                    positions.append([i, j])  # need to be tuple
        return positions
    
    def validCombinations(self):
        pos = self.availablePositions()
        mes = self.measured()
        placed = self.placed()
        combs = [['p', p] for p in pos]
        for i in placed:
            if i not in mes:
                combs.append(['m', i])
                for j in placed:
                    if j == i:
                        continue
                    if j not in mes:
                        combs.append(['e', [i,j]])
        random.shuffle(combs)
        return combs

    def updateState(self, position, act='m'):
        if act == 'e':
          self.board[position[0][0]][position[0][1]].entangle(self.board[position[1][0]][position[1][1]], self.embsym)
          self.embsym += 1
          return
        if act == 'p':
          self.board[position[0]][position[1]] = Symb(pos=[position[0],position[1]])
          return
        self.board[position[0]][position[1]].measure()

    def giveReward(self):
        result = self.winner()
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.5)
            self.p2.feedReward(0.5)

    def reset(self):
        self.board = [[Symb(empty=True) for i in range(self.col)] for j in range(self.row)]
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1
        self.embsym = 2

    def play(self, rounds=100):
        for i in range(rounds):
            if i%1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                avl_combs = self.validCombinations()
                p1_action, pos = self.p1.chooseAction(avl_combs, self.board)
                self.updateState(pos, p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)

                win = self.winner()
                if win is not None:
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    avl_combs = self.validCombinations()
                    p2_action, pos = self.p2.chooseAction(avl_combs, self.board)
                    self.updateState(pos, p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def play2(self):
        print("\n\nINFORMATION\n# => unmeasured qubit \n"
             +"number > 2 => entangled bit (two bits with same number are entangled) \n"
             + f"rows: 0 to {self.row-1}, columns: 0 to {self.col-1}\n""")
        if isinstance(self.p1, HumanPlayer):
            self.showBoard()
        while not self.isEnd:
            if isinstance(self.p1,HumanPlayer):
                p1_action, pos = self.p1.chooseAction(self.board)
            else:
                avl_combs = self.validCombinations()
                p1_action, pos = self.p1.chooseAction(avl_combs, self.board)
            self.updateState(pos, p1_action)
            self.showBoard()
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                elif win == -1:
                    print(self.p2.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                if isinstance(self.p2,HumanPlayer):
                    p2_action, pos = self.p2.chooseAction(self.board)
                else:
                    avl_combs = self.validCombinations()
                    p2_action, pos = self.p2.chooseAction(avl_combs, self.board)

                self.updateState(pos, p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    elif win == 1:
                        print(self.p1.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break
    def pvp(self):
        print("\n\nINFORMATION\n# => unmeasured qubit \n"
             +"number > 2 => entangled bit (two bits with same number are entangled) \n"
             + f"rows: 0 to {self.row-1}, columns: 0 to {self.col-1}\n""")
        self.showBoard()
        while not self.isEnd:
            p1_action, pos = self.p1.chooseAction(self.board)
            self.updateState(pos, p1_action)
            self.showBoard()
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                elif win == -1:
                    print(self.p2.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                p2_action, pos = self.p2.chooseAction(self.board)

                self.updateState(pos, p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    elif win == 1:
                        print(self.p1.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def showBoard(self):
        for i in range(0, self.row):
            print('-------------')
            out = '| '
            for j in range(0, self.col):
                if self.board[i][j].val == 1:
                    token = 'x'
                elif self.board[i][j].val == -1:
                    token = 'O'
                elif self.board[i][j].val == 0 and self.board[i][j].entangled:
                    token = str(self.board[i][j].symbol)
                elif self.board[i][j].val == 0 and not self.board[i][j].empty:
                    token = '#'
                else:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')