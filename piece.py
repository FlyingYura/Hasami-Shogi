class Piece:
    def __init__(self, color):
        self.color = color  

    def capture(self, board, x, y, captured_pieces):
        if board.is_empty(x, y):
            return False  
        opponent_piece = board.get_piece(x, y)
        if opponent_piece.color != self.color:
            board.remove_piece(x, y)  
            if self.color == "white":
                captured_pieces["white"].append(opponent_piece)
            else:
                captured_pieces["black"].append(opponent_piece)
            return True
        else:
            return False  