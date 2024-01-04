class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self,board):
        while True:
            act = input('Choose action (p: place bit, m: measure, e:entangle): ')
            if act not in ['p', 'm', 'e']:
               print('Please enter proper action (p or m or e)')
               continue
            try:  
              if act == 'e':
                f = input('Enter coordinates of first bit seperated by space i.e row col: ').split()
                f = [int(i) for i in f]
                s = input('Same for second bit : ').split()
                s = [int(i) for i in s]
                if board[f[0]][f[1]].val == 0 and not board[f[0]][f[1]].empty and board[f[0]][f[1]].val == 0 and not board[f[0]][f[1]].empty:
                  return act, [f,s]
                print('Enter valid action and coordinates!')
                continue

              pos = input('Enter coordinates of the bit seperated by space i.e row col: ').split()
              pos = [int(i) for i in pos]
              print(' ')
              if act == 'm':
                if board[pos[0]][pos[1]].val == 0 and not board[pos[0]][pos[1]].empty:
                  # print('y')
                  return act, pos

              elif board[pos[0]][pos[1]].empty:
                return act, pos
              print('Enter valid action and coordinates!')
            except:
               print('Enter valid action and coordinates!')

    def addState(self, state):
        pass

    def feedReward(self, reward):
        pass

    def reset(self):
        pass