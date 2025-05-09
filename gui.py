import tkinter as tk
from tkinter import messagebox
import numpy as np
from game import UltimateTicTacToe
from ai import UltimateTicTacToeAI

class UltimateTicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ultimate Tic Tac Toe")
        self.root.geometry("800x800")
        self.colors = {
            'background': '#f0f0f0',
            'board': '#ffffff',
            'available': '#e6f7ff',
            'unavailable': '#f5f5f5',
            'won_x': '#ffecec',  # Light red for X wins
            'won_o': '#ecfffe',  # Light blue for O wins
            'X': '#ff6b6b',  
            'O': '#4ecdc4', 
            'text': '#333333'
        }
        self.game = UltimateTicTacToe()
        self.ai = UltimateTicTacToeAI(depth=3)
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.main_frame.pack(expand=True, fill='both')
        self.buttons = [[[[None for _ in range(3)] for _ in range(3)] 
                        for _ in range(3)] for _ in range(3)]
        self.board_frames = [[None for _ in range(3)] for _ in range(3)]
        self.board_labels = [[None for _ in range(3)] for _ in range(3)]
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Create the welcome screen with game introduction."""
        welcome_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        welcome_frame.pack(expand=True, fill='both')
        
        title_label = tk.Label(
            welcome_frame,
            text="Ultimate Tic Tac Toe",
            font=('Arial', 24, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        title_label.pack(pady=20)
        
        rules_text = """
        Welcome to Ultimate Tic Tac Toe!
        
        Rules:
        1. You play as X (red) against the AI as O (blue)
        2. The game consists of nine 3x3 boards
        3. Win three small boards in a row to win the game
        4. You can play in any unfinished board
        5. When you win a board, you get another turn!
        
        Click 'Start Game' to begin!
        """
        
        rules_label = tk.Label(
            welcome_frame,
            text=rules_text,
            font=('Arial', 12),
            bg=self.colors['background'],
            fg=self.colors['text'],
            justify='left'
        )
        rules_label.pack(pady=20)
        
        start_button = tk.Button(
            welcome_frame,
            text="Start Game",
            font=('Arial', 14),
            bg=self.colors['X'],
            fg='white',
            command=self.start_game
        )
        start_button.pack(pady=20)

    def start_game(self):
        """Start the game and create the game board."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.create_game_board()
        self.update_board_appearance()

    def create_game_board(self):
        """Create the game board GUI."""
        self.status_label = tk.Label(
            self.main_frame,
            text="Your turn (X)",
            font=('Arial', 14, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        self.status_label.pack(pady=10)
        board_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        board_frame.pack(expand=True, fill='both', padx=20, pady=20)
        for i in range(3):
            for j in range(3):
                small_board_frame = tk.Frame(
                    board_frame,
                    bg=self.colors['board'],
                    highlightbackground="black",
                    highlightthickness=1
                )
                small_board_frame.grid(row=i, column=j, padx=5, pady=5)
                self.board_frames[i][j] = small_board_frame
                win_label = tk.Label(
                    small_board_frame,
                    text="",
                    font=('Arial', 48, 'bold'),
                    bg=self.colors['board']
                )
                self.board_labels[i][j] = win_label
                for x in range(3):
                    for y in range(3):
                        button = tk.Button(
                            small_board_frame,
                            text="",
                            font=('Arial', 16, 'bold'),
                            width=3,
                            height=1,
                            command=lambda i=i, j=j, x=x, y=y: self.make_move(i, j, x, y)
                        )
                        button.grid(row=x, column=y, padx=1, pady=1)
                        self.buttons[i][j][x][y] = button

    def update_board_appearance(self):
        """Update the appearance of all boards based on game state."""
        valid_moves = self.game.get_valid_moves()
        current_turn = "Your" if self.game.current_player == -1 else "AI's"
        current_symbol = "X" if self.game.current_player == -1 else "O"
        self.status_label.config(text=f"{current_turn} turn ({current_symbol})")
        
        for i in range(3):
            for j in range(3):
                if self.game.main_board[i, j] != 0:
                    for x in range(3):
                        for y in range(3):
                            self.buttons[i][j][x][y].grid_remove()
                    win_label = self.board_labels[i][j]
                    win_label.config(
                        text="X" if self.game.main_board[i, j] == -1 else "O",
                        fg=self.colors['X'] if self.game.main_board[i, j] == -1 else self.colors['O']
                    )
                    win_label.grid(row=0, column=0, rowspan=3, columnspan=3, sticky='nsew')
                    self.board_frames[i][j].config(
                        bg=self.colors['won_x'] if self.game.main_board[i, j] == -1 else self.colors['won_o']
                    )
                    win_label.config(
                        bg=self.colors['won_x'] if self.game.main_board[i, j] == -1 else self.colors['won_o']
                    )
                else:
                    for x in range(3):
                        for y in range(3):
                            button = self.buttons[i][j][x][y]
                            cell_value = self.game.small_boards[i, j, x, y]
                            if cell_value == -1:  
                                button.config(text="X", fg=self.colors['X'])
                            elif cell_value == 1:  
                                button.config(text="O", fg=self.colors['O'])
                            else:
                                button.config(text="")
                            if (i, j, x, y) in valid_moves and self.game.current_player == -1:
                                button.config(state=tk.NORMAL, bg=self.colors['available'])
                            else:
                                button.config(state=tk.DISABLED, bg=self.colors['board'])
        if self.game.current_player == 1 and not self.game.is_game_over():
            self.root.after(500, self.process_ai_move)

    def make_move(self, i: int, j: int, x: int, y: int):
        """Handle player move and update GUI."""
        if self.game.make_move((i, j, x, y)):
            self.update_board_appearance()
            if self.game.is_game_over():
                self.show_game_over()

    def process_ai_move(self):
        """Process AI move and update the game state."""
        move = self.ai.get_best_move(self.game)
        if move:
            if self.game.make_move(move):
                self.update_board_appearance()
                if self.game.is_game_over():
                    self.show_game_over()

    def show_game_over(self):
        """Show game over message and handle end of game."""
        winner = self.game.get_winner()
        if winner == 1:
            messagebox.showinfo("Game Over", "AI wins!")
        elif winner == -1:
            messagebox.showinfo("Game Over", "You win!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        self.root.quit()

    def run(self):
        """Start the GUI application."""
        self.root.mainloop() 