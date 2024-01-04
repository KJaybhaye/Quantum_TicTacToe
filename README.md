# Quantum_TicTacToe
A simple TicTacToe with some Quantum Mechanics concepts.

## Rules:
1) Each player can perform one 3 actions: a) place a quantum symbol b) entangle two symbols c) measure one of the placed symbols
2) Quantum symbol: This is a symbol that is in superposition of both 'X' and 'O'.
3) Measurement: When measured it collapses to one of the two symbols.
4) Entangled symbols: When one of the entangled symbols is measured it collapses to a symbol. The symbol entangled with it becomes the opposite symbol.
5) Winning: Similar to normal TicTacToe.


Player can play against the computer or against another player.

## Computer Player
Basic Reinforcement Learning models are trained to play the game.


## How to play
Install required packeges(given in requirements.txt)
Run main.py

## Training models with custom difficulty
Change number of rounds in 'rounds' list in train.py (higher the rounds higher the difficulty)
Run train.py
