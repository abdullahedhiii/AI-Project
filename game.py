import numpy as np
from typing import Tuple, List, Optional

class UltimateTicTacToe:
    def __init__(self):
        self.main_board = np.zeros((3, 3), dtype=int)
        self.small_boards = np.zeros((3, 3, 3, 3), dtype=int)
        self.current_player = -1  
        self.game_over = False
        self.winner = 0

    def get_valid_moves(self) -> List[Tuple[int, int, int, int]]:
        """Get all valid moves for the current player."""
        valid_moves = []
        for i in range(3):
            for j in range(3):
                if self.main_board[i, j] == 0:  
                    for x in range(3):
                        for y in range(3):
                            if self.small_boards[i, j, x, y] == 0:
                                valid_moves.append((i, j, x, y))
        return valid_moves

    def make_move(self, move: Tuple[int, int, int, int]) -> bool:
        """Make a move and update game state."""
        i, j, x, y = move
        valid_moves = self.get_valid_moves()
        if move not in valid_moves:
            return False
        self.small_boards[i, j, x, y] = self.current_player
        board_won = False
        if self._check_small_board_win(i, j):
            self.main_board[i, j] = self.current_player
            board_won = True
            if self._check_main_board_win():
                self.game_over = True
                self.winner = self.current_player
                return True
        if not board_won:
            self.current_player *= -1

        return True

    def _check_small_board_win(self, i: int, j: int) -> bool:
        """Check if a small board is won."""
        board = self.small_boards[i, j]
        for row in range(3):
            if abs(sum(board[row])) == 3:
                return True
        for col in range(3):
            if abs(sum(board[:, col])) == 3:
                return True
        if abs(sum(board.diagonal())) == 3:
            return True
        if abs(sum(np.fliplr(board).diagonal())) == 3:
            return True
        return False

    def _check_main_board_win(self) -> bool:
        """Check if the main board is won."""
        for row in range(3):
            if abs(sum(self.main_board[row])) == 3:
                return True
        for col in range(3):
            if abs(sum(self.main_board[:, col])) == 3:
                return True
        if abs(sum(self.main_board.diagonal())) == 3:
            return True
        if abs(sum(np.fliplr(self.main_board).diagonal())) == 3:
            return True
        return False

    def is_game_over(self) -> bool:
        return self.game_over or len(self.get_valid_moves()) == 0

    def get_winner(self) -> int:
        return self.winner

    def get_board_state(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.main_board.copy(), self.small_boards.copy() 