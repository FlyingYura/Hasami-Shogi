import tkinter as tk
from tkinter import messagebox
from ctypes import cdll, c_int, c_bool, POINTER
import time

SIZE = 9  # Розмір дошки

# Завантаження C++ DLL
try:
    hasami_dll = cdll.LoadLibrary('./hasami_shogi.dll')  # Потрібно скоригувати шлях до DLL
    hasami_dll.is_empty.argtypes = [POINTER(c_int), c_int, c_int]
    hasami_dll.is_empty.restype = c_bool
except Exception as e:
    print(f"Error loading DLL: {e}")
    exit(1)

# Ініціалізація ігрової дошки
board = [[0] * SIZE for _ in range(SIZE)]


class HasamiShogi:
    def __init__(self, root):
        self.root = root
        self.root.title("Hasami Shogi")
        self.turn = 1  # 1 для гравця 1, -1 для гравця 2
        self.timer_start = time.time()

        # Рами для дошки та інформації
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.captured_frame_left = tk.Frame(self.main_frame, width=100, bg="white")
        self.captured_frame_left.pack(side=tk.LEFT, fill=tk.Y)

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.LEFT)

        self.captured_frame_right = tk.Frame(self.main_frame, width=100, bg="white")
        self.captured_frame_right.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_frame = tk.Frame(root)
        self.info_frame.pack()

        # Індикатор ходу та таймер
        self.turn_label = tk.Label(self.info_frame, text="Player 1's Turn (White)", font=("Arial", 14))
        self.turn_label.pack(side=tk.LEFT, padx=20)
        self.timer_label = tk.Label(self.info_frame, text="Time: 0s", font=("Arial", 14))
        self.timer_label.pack(side=tk.LEFT, padx=20)

        # Кнопка завершення гри
        self.reset_button = tk.Button(self.info_frame, text="Reset Game", command=self.reset_game, font=("Arial", 14))
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        # Ініціалізація клітинок
        self.cells = [[None for _ in range(SIZE)] for _ in range(SIZE)]
        self.selected_piece = None
        self.initialize_board()

        # Захоплені фігури
        self.captured_white = []  # Збиті білі фігури
        self.captured_black = []  # Збиті чорні фігури

        # Оновлення таймера
        self.update_timer()

    def initialize_board(self):
        for i in range(SIZE):
            for j in range(SIZE):
                color = "beige" if (i + j) % 2 == 0 else "wheat"
                canvas = tk.Canvas(self.board_frame, bg=color, width=90, height=90, highlightthickness=1,
                                   highlightbackground="black")
                canvas.grid(row=i, column=j)
                canvas.bind("<Button-1>", lambda event, x=i, y=j: self.cell_clicked(x, y))
                self.cells[i][j] = canvas
                # Ініціалізація фігур
                if i == 0:
                    self.place_piece(i, j, "black")
                    board[i][j] = -1  # Фігури гравця 2
                elif i == SIZE - 1:
                    self.place_piece(i, j, "white")
                    board[i][j] = 1  # Фігури гравця 1

    def place_piece(self, x, y, color):
        radius = 35  # Розмір фігур
        self.cells[x][y].create_oval(10, 10, 80, 80, fill=color, outline="")

    def remove_piece(self, x, y):
        self.cells[x][y].delete("all")

    def add_captured_piece(self, color):
        # Додати збиту фігурку до відповідного списку
        frame = self.captured_frame_right if color == "white" else self.captured_frame_left
        canvas = tk.Canvas(frame, width=60, height=60, bg="white", highlightthickness=0)
        canvas.pack(pady=5)
        canvas.create_oval(10, 10, 50, 50, fill=color, outline="")
        if color == "white":
            self.captured_white.append(canvas)
        else:
            self.captured_black.append(canvas)

    def cell_clicked(self, x, y):
        if self.selected_piece:
            if self.is_valid_move(self.selected_piece[0], self.selected_piece[1], x, y):
                self.make_move(self.selected_piece[0], self.selected_piece[1], x, y)
                self.check_win_condition()
                self.end_turn()
            self.selected_piece = None
        else:
            if board[x][y] == self.turn:
                self.selected_piece = (x, y)

    def is_valid_move(self, x1, y1, x2, y2):
        if (x1 == x2 or y1 == y2) and board[x2][y2] == 0:
            board_pointer = (c_int * (SIZE * SIZE))(*sum(board, []))
            if hasami_dll.is_empty(board_pointer, x2, y2):
                return True
        return False

    def make_move(self, x1, y1, x2, y2):
        color = "white" if self.turn == 1 else "black"
        self.remove_piece(x1, y1)
        board[x1][y1] = 0
        self.place_piece(x2, y2, color)
        board[x2][y2] = self.turn
        self.capture_pieces(x2, y2)

    def capture_pieces(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            self.capture_in_direction(x, y, dx, dy)

    def capture_in_direction(self, x, y, dx, dy):
        opponent = -self.turn
        nx, ny = x + dx, y + dy
        captured = []
        while 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] == opponent:
            captured.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] == self.turn:
            for cx, cy in captured:
                board[cx][cy] = 0
                color = "white" if opponent == 1 else "black"
                self.add_captured_piece(color)
                self.remove_piece(cx, cy)

    def check_win_condition(self):
        white_pieces = sum(row.count(1) for row in board)
        black_pieces = sum(row.count(-1) for row in board)
        if white_pieces == 0:
            messagebox.showinfo("Game Over", "Player 2 (Black) wins!")
            self.reset_game()
        elif black_pieces == 0:
            messagebox.showinfo("Game Over", "Player 1 (White) wins!")
            self.reset_game()

    def reset_game(self):
        for i in range(SIZE):
            for j in range(SIZE):
                self.remove_piece(i, j)
                board[i][j] = 0
        for frame in [self.captured_frame_left, self.captured_frame_right]:
            for widget in frame.winfo_children():
                widget.destroy()
        self.captured_white.clear()
        self.captured_black.clear()
        self.initialize_board()
        self.turn = 1
        self.update_turn_label()

    def update_turn_label(self):
        self.turn_label.config(text=f"{'Player 1 (White)' if self.turn == 1 else 'Player 2 (Black)'}'s Turn")

    def update_timer(self):
        elapsed_time = int(time.time() - self.timer_start)
        self.timer_label.config(text=f"Time: {elapsed_time}s")
        self.root.after(1000, self.update_timer)

    def end_turn(self):
        self.turn *= -1
        self.update_turn_label()
        self.timer_start = time.time()

if __name__ == "__main__":
    root = tk.Tk()
    game = HasamiShogi(root)
    root.mainloop()
