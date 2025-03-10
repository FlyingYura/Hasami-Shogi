import tkinter as tk
from ctypes import cdll, c_int, c_bool, POINTER
from PIL import Image, ImageTk  
import time

SIZE = 9  

try:
    hasami_dll = cdll.LoadLibrary('./hasami_shogi.dll')  
    hasami_dll.is_empty.argtypes = [POINTER(c_int), c_int, c_int]
    hasami_dll.is_empty.restype = c_bool
except Exception as e:
    print(f"Error loading DLL: {e}")
    exit(1)

class Board:
    
    def __init__(self):
        self.turn_value = 1
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.cells = [[None for _ in range(SIZE)] for _ in range(SIZE)]
        
        self.white_piece_icon = ImageTk.PhotoImage(Image.open("icons/white_piece.png").resize((80, 80)))
        self.black_piece_icon = ImageTk.PhotoImage(Image.open("icons/black_piece.png").resize((80, 80)))

    def place_piece(self, x, y, color):
        image = self.white_piece_icon if color == "white" else self.black_piece_icon
        self.cells[x][y].create_image(45, 45, image=image) 

    def remove_piece(self, x, y):
        self.cells[x][y].delete("all")

    def is_empty(self, x, y):
        board_pointer = (c_int * (SIZE * SIZE))(*sum(self.board, []))
        return hasami_dll.is_empty(board_pointer, x, y)

    def capture_pieces(self, x, y, turn):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            self.capture_in_direction(x, y, dx, dy, turn)

    def capture_in_direction(self, x, y, dx, dy, turn):
        opponent = -turn
        nx, ny = x + dx, y + dy
        captured = []

        # Шукаємо фігури супротивника в напрямку (dx, dy)
        while 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx][ny] == opponent:
            captured.append((nx, ny))
            nx += dx
            ny += dy

        # Перевірка, чи в кінці ланцюга є фігура нашого кольору
        if 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx][ny] == turn:
            for cx, cy in captured:
                self.board[cx][cy] = 0  
                self.remove_piece(cx, cy)  
        else:
            # Якщо після ланцюга супротивників немає нашої фігури, не захоплюємо
            return

    def reset_board(self):
        """Скидання дошки"""
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.cells = [[None for _ in range(SIZE)] for _ in range(SIZE)]
