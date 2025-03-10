import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from board import Board
from player import Player
from ai import AIPlayer

SIZE = 9


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Hasami Shogi")
        self.root.configure(bg="#f5f5f5")  

        self.root.attributes("-fullscreen", True)

        self.turn = 1  
        self.timer_start = time.time()

        self.white_piece_icon = ImageTk.PhotoImage(Image.open("icons/white_piece.png").resize((80, 80)))
        self.black_piece_icon = ImageTk.PhotoImage(Image.open("icons/black_piece.png").resize((80, 80)))

        self.board = Board()
        self.player1 = Player("white", "Player 1")
        self.player2 = Player("black", "Player 2")

        self.ai = AIPlayer("black", "easy")

        # Рамки для дошки
        self.main_frame = tk.Frame(root, bg="#f5f5f5")
        self.main_frame.pack()

        self.captured_frame_left = tk.Frame(self.main_frame, width=120, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.captured_frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.board_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.board_frame.pack(side=tk.LEFT, padx=10)

        self.captured_frame_right = tk.Frame(self.main_frame, width=120, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.captured_frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.info_frame = tk.Frame(root, bg="#f5f5f5")
        self.info_frame.pack(pady=10)

        self.timer_label = tk.Label(self.info_frame, text="Time: 0s", font=("Arial", 16, "bold"), bg="#f5f5f5")
        self.timer_label.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(self.info_frame, text="Reset Game", command=self.reset_game, font=("Arial", 14), bg="#ffccbc", fg="black")
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        self.back_to_menu_button = tk.Button(self.info_frame, text="Back to Menu", command=self.back_to_menu, font=("Arial", 14), bg="#ffccbc", fg="black")
        self.back_to_menu_button.pack(side=tk.LEFT, padx=10)

        self.win_message_label = tk.Label(self.main_frame, text="", font=("Arial", 20, "bold"), bg="#f5f5f5", fg="green")
        self.win_message_label.pack(side=tk.BOTTOM, pady=20)  

        self.exit_fullscreen_button = tk.Button(self.info_frame, text="Exit Fullscreen", command=self.toggle_fullscreen, font=("Arial", 14), bg="#ffccbc", fg="black")
        self.exit_fullscreen_button.pack(side=tk.LEFT, padx=10)

        self.start_game()
        self.timer_update()

        self.selected_piece = None
        self.initialize_board()

    def toggle_fullscreen(self):
        is_fullscreen = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fullscreen)

    def back_to_menu(self):
        from menu import MainMenu
        self.root.destroy()  
        menu_root = tk.Tk()  
        menu = MainMenu(menu_root)  
        menu_root.mainloop() 

    def reset_game(self):
        self.board.reset_board()  
        self.player1.captured_pieces.clear()
        self.player2.captured_pieces.clear()
        self.initialize_board()  
        self.turn = 1  # 
        self.timer_start = time.time() 

    def initialize_board(self):

        for j in range(SIZE):
            label = tk.Label(self.board_frame, text=chr(65 + j), font=("Arial", 12, "bold"), bg="#f5f5f5")
            label.grid(row=0, column=j + 1, padx=5, pady=5, sticky="nsew") 

        for j in range(SIZE):
            label = tk.Label(self.board_frame, text=chr(65 + j), font=("Arial", 12, "bold"), bg="#f5f5f5")
            label.grid(row=SIZE + 1, column=j + 1, padx=5, pady=5, sticky="nsew")  

        for i in range(SIZE):
            label = tk.Label(self.board_frame, text=str(i + 1), font=("Arial", 12, "bold"), bg="#f5f5f5")
            label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="nsew") 

        for i in range(SIZE):
            label = tk.Label(self.board_frame, text=str(i + 1), font=("Arial", 12, "bold"), bg="#f5f5f5")
            label.grid(row=i + 1, column=SIZE + 1, padx=5, pady=5, sticky="nsew")  

        # Створення дошки
        for i in range(SIZE):
            for j in range(SIZE):
                color = "#ffebcd" if (i + j) % 2 == 0 else "#d2b48c"
                canvas = tk.Canvas(self.board_frame, bg=color, width=90, height=90, highlightthickness=1,
                                highlightbackground="black")
                canvas.grid(row=i + 1, column=j + 1)  # Зсув, щоб зробити місце для розмітки
                canvas.bind("<Button-1>", lambda event, x=i, y=j: self.cell_clicked(x, y))
                self.board.cells[i][j] = canvas

                if i == 0:
                    self.board.place_piece(i, j, "black")
                    self.board.board[i][j] = -1
                    canvas.create_image(45, 45, image=self.black_piece_icon)
                elif i == SIZE - 1:
                    self.board.place_piece(i, j, "white")
                    self.board.board[i][j] = 1
                    canvas.create_image(45, 45, image=self.white_piece_icon)

    def cell_clicked(self, x, y):
        if self.selected_piece:
            if self.is_valid_move(self.selected_piece[0], self.selected_piece[1], x, y):
                self.make_move(self.selected_piece[0], self.selected_piece[1], x, y)
                self.check_win_condition()
                self.end_turn()
            self.selected_piece = None
        else:
            if self.board.board[x][y] == self.turn:
                self.selected_piece = (x, y)

    def is_valid_move(self, x1, y1, x2, y2):
        if (x1 == x2 or y1 == y2) and self.board.board[x2][y2] == 0:
            if self.board.is_empty(x2, y2):
                return True
        return False
    def make_move(self, x1, y1, x2, y2):
        self.board.cells[x1][y1].delete("all")

        # Додавання зображення на нову клітинку
        color = "white" if self.turn == 1 else "black"
        self.board.place_piece(x2, y2, color)
        icon = self.white_piece_icon if self.turn == 1 else self.black_piece_icon
        self.board.cells[x2][y2].create_image(45, 45, image=icon)

        self.board.board[x1][y1] = 0
        self.board.board[x2][y2] = self.turn

        # Виклик захоплення фігур після переміщення
        self.board.capture_pieces(x2, y2, self.turn)

    def check_win_condition(self):
        white_pieces = sum(row.count(1) for row in self.board.board)
        black_pieces = sum(row.count(-1) for row in self.board.board)

        if white_pieces == 1:
            self.display_win_message("You lost!")
            self.reset_game()
        elif black_pieces == 1:
            self.display_win_message("You won!")
            self.reset_game()

    def display_win_message(self, message):
        """Функція для відображення повідомлення про перемогу в основному вікні."""
        self.win_message_label.config(text=message, fg="red")  
        self.win_message_label.after(3000, self.clear_win_message)  

    def clear_win_message(self):
        """Очищує повідомлення про перемогу після певного часу."""
        self.win_message_label.config(text="")

    def start_timer(self):
        if not hasattr(self, 'timer_running') or not self.timer_running:
            self.timer_running = True
            self.timer_start = time.time()  
            self.timer_update()  

    def stop_timer(self):
        self.timer_running = False
        self.time_elapsed = 0  
        self.timer_label.config(text="Time: 0s")

    def reset_timer(self):
        self.time_elapsed = 0
        self.timer_label.config(text="Time: 0s")
        self.stop_timer()  

    def timer_update(self):
        if self.timer_running:
            elapsed = int(time.time() - self.timer_start)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.timer_label.after(1000, lambda: self.timer_update())  

    def end_turn(self):
        self.turn = -self.turn 
        self.timer_start = time.time()  

        if self.turn == -1:
            print("AI's turn")
            move = self.ai.make_move(self.board)  
            print(f"AI move: {move}")  
            if move:
                x1, y1, x2, y2 = move
                self.make_move(x1, y1, x2, y2)
                self.check_win_condition()
            self.end_turn()
        else:
            self.reset_timer()  
            self.start_timer()  

    def start_game(self):
        self.reset_timer()
        self.start_timer()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    game.timer_update()
    root.mainloop()
