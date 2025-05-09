# Ultimate Tic Tac Toe

A Python implementation of Ultimate Tic Tac Toe with an AI opponent using the Minimax algorithm with alpha-beta pruning.

## Description

Ultimate Tic Tac Toe is an advanced variation of the classic Tic Tac Toe game. It consists of a 3x3 grid of smaller Tic Tac Toe boards, making it a more strategic and challenging game. The AI opponent uses the Minimax algorithm with alpha-beta pruning for optimal move selection.

## Features

- Modern GUI using tkinter
- AI opponent using Minimax with alpha-beta pruning
- Welcome screen with game rules
- Interactive game board
- Win detection and game over handling

## Requirements

- Python 3.7+
- numpy
- tkinter (usually comes with Python)

## Installation

1. Clone the repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```
2. Read the rules on the welcome screen
3. Click "Start Game" to begin
4. Make your moves by clicking on the desired cell
5. The game will automatically handle turns between you and the AI

## Game Rules

1. The game consists of nine 3x3 boards, arranged to form a larger 3x3 grid
2. Each cell of the main board contains its own 3x3 board
3. A player must win three small boards in a row (horizontally, vertically, or diagonally) to win the game
4. Your move determines which board the opponent plays in next
5. If a board is already won, you can play in any available board

## AI Implementation

The AI uses the Minimax algorithm with alpha-beta pruning to evaluate moves. The evaluation function considers:
- Mini board control
- Win potential within mini boards
- Main board win opportunities
- Center control

## License

This project is open source and available under the MIT License. 