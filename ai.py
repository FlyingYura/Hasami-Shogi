import random
SIZE = 9
class AIPlayer:
    def __init__(self, color, difficulty):
        self.color = color
        self.difficulty = difficulty  
        self.turn_value = 1 if color == "white" else -1  

    def make_move(self, board):
        if self.difficulty == "easy":
            return self.make_easy_move(board)
        else:
            return self.make_hard_move(board)
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def make_easy_move(self, board):
        possible_moves = []
        for i in range(SIZE):
            for j in range(SIZE):
                if board.board[i][j] == self.turn_value:
                    for x in range(SIZE):
                        for y in range(SIZE):
                            if board.is_empty(x, y) and self.is_valid_move(i, j, x, y, board):
                                possible_moves.append((i, j, x, y))

        if possible_moves:
            move = random.choice(possible_moves)
            return move
        return None

    def make_hard_move(self, board):
        best_move = None
        best_score = -float('inf')

        for i in range(SIZE):
            for j in range(SIZE):
                if board.board[i][j] == self.turn_value:
                    for x in range(SIZE):
                        for y in range(SIZE):
                            if board.is_empty(x, y) and self.is_valid_move(i, j, x, y, board):
                                score = self.evaluate_move(board, i, j, x, y)
                                if score > best_score:
                                    best_score = score
                                    best_move = (i, j, x, y)

        return best_move

    def is_valid_move(self, x1, y1, x2, y2, board):
        return (x1 == x2 or y1 == y2) and board.is_empty(x2, y2)

    def evaluate_move(self, board, x1, y1, x2, y2):
        score = 0
        board_copy = [row.copy() for row in board.board]  
        board_copy[x2][y2] = board.turn_value
        captured_pieces = self.capture_pieces(board_copy, x2, y2)
        score += len(captured_pieces)  

        if self.check_win(board_copy):
            score += 100  

        return score

    def capture_pieces(self, board, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        captured = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            captured_in_direction = []
            while 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] == -self.turn_value:
                captured_in_direction.append((nx, ny))
                nx += dx
                ny += dy

            if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] == self.turn_value:
                captured.extend(captured_in_direction)

        return captured

    def check_win(self, board):
        """Перевірка на виграш."""
        white_pieces = sum(row.count(1) for row in board)
        black_pieces = sum(row.count(-1) for row in board)
        return white_pieces == 0 or black_pieces == 0