from human import HumanPlayer
from player import Player
from state import State


while True:
    pl_1 = input("Choose player 1 (c for computer, h for human): ")
    if pl_1 not in ['c', 'h']:
        print('Enter valid input (c or h).')
        continue
    if pl_1 == 'c':
        p1 = Player("computer_p1", exp_rate=0)
        try:
            inp = int(input('Select difficulty (very easy: 0, easy: 1, normal: 2, difficult: 3, very difficult: 4 ): '))
            p1.loadPolicy('./Policies/policy_p1' + f'_{inp}')
            print(f'Symbol for computer_p1: X')
            break
        except:
            print('Enter valid input')
            continue
    else:
        inp = input("Enter name : ")
        p1 = HumanPlayer(inp)
        print(f'Symbol for {inp}: X')
        break

while True:
    pl_2 = input("Choose player 2 (c for computer, h for human): ")
    if pl_2 not in ['c', 'h']:
        print('Enter valid input (c or h).')
        continue
    if pl_2 == 'c':
        p2 = Player("computer_p2", exp_rate=0)
        try:
            inp = int(input('Select difficulty (very easy: 0, easy: 1, normal: 2, difficult: 3, very difficult: 4 ): '))
            p2.loadPolicy('./Policies/policy_p2' + f'_{inp}')
            print(f'Symbol for computer_p1: O')
            break
        except:
            print('Enter valid input')
            continue
    else:
        inp = input("Enter name : ")
        p2 = HumanPlayer(inp)
        print(f'Symbol for {inp}: O')
        break

st = State(p1, p2)

if pl_1 == 'h' and pl_2 == 'h':
    st.pvp()
else:
    st.play2()
