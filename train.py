from player import Player
from state import State

p1 = Player("p1")
p2 = Player("p2")

st = State(p1, p2)
print("training...")

rounds = [500, 1500, 4000, 8000, 15000]
# p1_names = []
inp = int(input('Enter model type (very easy: 0, easy: 1, normal: 2, difficult: 3, very difficult: 4 ): '))

st.play(rounds[inp])

p1.savePolicy(inp)
p2.savePolicy(inp)