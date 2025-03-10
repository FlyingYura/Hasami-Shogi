class Player:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.captured_pieces = []
        self.turn_value = 1 if color == "white" else -1  