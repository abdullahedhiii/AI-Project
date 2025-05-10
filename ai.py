import numpy as np
from typing import Tuple, List, Optional
from game import UltimateTicTacToe
import time

class UltimateTicTacToeAI:
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.time_taken = []
        self.last_board_played_in = None
    
    def get_average_time_taken(self):
        sum = 0
        for t in self.time_taken:
            sum+=t
            
        return sum/len(self.time_taken)
        
    def evaluate_board(self, game: UltimateTicTacToe) -> float:
        main_board, small_boards = game.get_board_state()
        score = 0
        for i in range(3):
            row_sum = sum(main_board[i])
            if abs(row_sum) == 3:
                return float('inf') if row_sum == 3 else float('-inf')
            col_sum = sum(main_board[:, i])
            if abs(col_sum) == 3:
                return float('inf') if col_sum == 3 else float('-inf')
        diag1 = sum(main_board.diagonal())
        diag2 = sum(np.fliplr(main_board).diagonal())
        if abs(diag1) == 3:
            return float('inf') if diag1 == 3 else float('-inf')
        if abs(diag2) == 3:
            return float('inf') if diag2 == 3 else float('-inf')
        position_weights = np.array([[3, 2, 3],
                                   [2, 4, 2],
                                   [3, 2, 3]])
        for i in range(3):
            for j in range(3):
                if main_board[i, j] == 1:  # AI wins
                    score += 100 * position_weights[i, j]
                elif main_board[i, j] == -1:  # Human wins
                    score -= 100 * position_weights[i, j]
        for i in range(3):
            for j in range(3):
                if main_board[i, j] == 0: 
                    board = small_boards[i, j]
                    for k in range(3):
                        row_sum = sum(board[k])
                        col_sum = sum(board[:, k])
                        if abs(row_sum) == 2 and row_sum < 0:
                            score -= 50
                        elif abs(row_sum) == 2 and row_sum > 0:
                            score += 30
                        if abs(col_sum) == 2 and col_sum < 0:
                            score -= 50
                        elif abs(col_sum) == 2 and col_sum > 0:
                            score += 30
                    diag1 = sum(board.diagonal())
                    diag2 = sum(np.fliplr(board).diagonal())
                    if abs(diag1) == 2 and diag1 < 0:
                        score -= 50
                    elif abs(diag1) == 2 and diag1 > 0:
                        score += 30
                    if abs(diag2) == 2 and diag2 < 0:
                        score -= 50
                    elif abs(diag2) == 2 and diag2 > 0:
                        score += 30
        for i in range(3):
            row_sum = sum(main_board[i])
            col_sum = sum(main_board[:, i])
            if abs(row_sum) == 2 and row_sum < 0:
                score -= 500
            elif abs(row_sum) == 2 and row_sum > 0:
                score += 400
            if abs(col_sum) == 2 and col_sum < 0:
                score -= 500
            elif abs(col_sum) == 2 and col_sum > 0:
                score += 400
        diag1 = sum(main_board.diagonal())
        diag2 = sum(np.fliplr(main_board).diagonal())
        if abs(diag1) == 2 and diag1 < 0:
            score -= 500
        elif abs(diag1) == 2 and diag1 > 0:
            score += 400
        if abs(diag2) == 2 and diag2 < 0:
            score -= 500
        elif abs(diag2) == 2 and diag2 > 0:
            score += 400

        return score

    def minimax(self, game: UltimateTicTacToe, depth: int, alpha: float, beta: float, 
                maximizing_player: bool) -> Tuple[float, Optional[Tuple[int, int, int, int]]]:
        if depth == 0 or game.is_game_over():
            return self.evaluate_board(game), None

        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return self.evaluate_board(game), None

        best_move = valid_moves[0]  
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                game_copy = UltimateTicTacToe()
                game_copy.main_board = game.main_board.copy()
                game_copy.small_boards = game.small_boards.copy()
                game_copy.current_player = game.current_player
                game_copy.make_move(move)
                eval, _ = self.minimax(game_copy, depth - 1, alpha, beta, False)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                game_copy = UltimateTicTacToe()
                game_copy.main_board = game.main_board.copy()
                game_copy.small_boards = game.small_boards.copy()
                game_copy.current_player = game.current_player
                game_copy.make_move(move)
                eval, _ = self.minimax(game_copy, depth - 1, alpha, beta, True)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self, game: UltimateTicTacToe) -> Optional[Tuple[int, int, int, int]]:
        if game.current_player != 1:  
            return None
        valid_moves = game.get_valid_moves(self.last_board_played_in)
        if not valid_moves:
            return None
        
        start_time = time.time()    
        _, best_move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        end_time = time.time()
        i, j, x, y = best_move

        self.last_board_played_in = (i, j, x, y)
        self.time_taken.append(end_time-start_time)
        return best_move 