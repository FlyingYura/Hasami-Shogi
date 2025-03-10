import tkinter as tk
from game import Game

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Hasami Shogi - Main Menu")
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg="#f7eac6")
        
        self.main_frame = tk.Frame(root, bg="#f7eac6")
        self.main_frame.pack(fill="both", expand=True)

      
        self.language = "ukrainian"  
        self.create_main_menu()

    def create_main_menu(self):
        """Створює головне меню."""
        self.clear_frame()

        title_label = tk.Label(self.main_frame, text=self.get_translation("Hasami Shogi"), font=("Gabriola", 58, "bold"), bg="#f7eac6", fg="#6d4c41")
        title_label.pack(pady=40)

        play_button = tk.Button(self.main_frame, text=self.get_translation("Play Game"), font=("Arial", 18, "bold"), bg="#c8e6c9", fg="black", command=self.show_difficulty_selection)
        play_button.pack(pady=20)

        rules_button = tk.Button(self.main_frame, text=self.get_translation("Rules of the Game"), font=("Arial", 18, "bold"), bg="#bbdefb", fg="black", command=self.show_rules)
        rules_button.pack(pady=20)

        change_language_button = tk.Button(self.main_frame, text=self.get_translation("Change Language"), font=("Arial", 18, "bold"), bg="#fff59d", fg="black", command=self.show_language_menu)
        change_language_button.pack(pady=20)

        exit_button = tk.Button(self.main_frame, text=self.get_translation("Exit Game"), font=("Arial", 18, "bold"), bg="#ef9a9a", fg="black", command=self.exit_game)
        exit_button.pack(pady=20)

    def show_language_menu(self):
        """Показує підменю для вибору мови."""
        self.clear_frame()

        language_label = tk.Label(self.main_frame, text=self.get_translation("Select Language"), font=("Gabriola", 42, "bold"), bg="#f7eac6", fg="#6d4c41")
        language_label.pack(pady=40)

        if self.language == "ukrainian":
            ukraine_button = tk.Button(self.main_frame, text=self.get_translation("English"), font=("Arial", 18, "bold"), bg="#c8e6c9", fg="black", command=self.change_language_to_english)
            ukraine_button.pack(pady=20)

            english_button = tk.Button(self.main_frame, text=self.get_translation("Ukrainian"), font=("Arial", 18, "bold"), bg="#c8e6c9", fg="black", command=self.change_language_to_ukrainian)
            english_button.pack(pady=20)
        else:
            ukraine_button = tk.Button(self.main_frame, text=self.get_translation("Ukrainian"), font=("Arial", 18, "bold"), bg="#c8e6c9", fg="black", command=self.change_language_to_ukrainian)
            ukraine_button.pack(pady=20)

            english_button = tk.Button(self.main_frame, text=self.get_translation("English"), font=("Arial", 18, "bold"), bg="#c8e6c9", fg="black", command=self.change_language_to_english)
            english_button.pack(pady=20)

        back_button = tk.Button(self.main_frame, text=self.get_translation("Back to Menu"), font=("Arial", 18, "bold"), bg="#ffccbc", fg="black", command=self.back_to_menu)
        back_button.pack(pady=20)

    def change_language_to_english(self):
        """Змінює мову на англійську."""
        self.language = "english"
        self.create_main_menu()

    def change_language_to_ukrainian(self):
        """Змінює мову на українську."""
        self.language = "ukrainian"
        self.create_main_menu()

    def get_translation(self, text):
        """Отримує переклад для певного тексту в залежності від мови."""
        translations = {
            "ukrainian": {
                "Hasami Shogi": "Хасамі Шогі",
                "Play Game": "Грати",
                "Rules of the Game": "Правила гри",
                "Exit Game": "Вийти",
                "Change Language": "Змінити мову",
                "Select Language": "Вибір мови",
                "English": "Англійська",
                "Ukrainian": "Українська",
                "Back to Menu": "Повернутися в меню",
                "Easy Mode": "Легкий рівень",
                "Hard Mode": "Складний рівень",
                "Select Difficulty": "Вибір складності",
                "Rules of Hasami Shogi": "Правила Хасамі Шогі",
                "Game Rules": "Правила гри"
            },
            "english": {
                "Hasami Shogi": "Hasami Shogi",
                "Play Game": "Play Game",
                "Rules of the Game": "Rules of the Game",
                "Exit Game": "Exit Game",
                "Change Language": "Change Language",
                "Select Language": "Select Language",
                "English": "English",
                "Ukrainian": "Ukrainian",
                "Back to Menu": "Back to Menu",
                "Easy Mode": "Easy Mode",
                "Hard Mode": "Hard Mode",
                "Select Difficulty": "Select Difficulty",
                "Rules of Hasami Shogi": "Rules of Hasami Shogi",
                "Game Rules": "Game Rules"
            }
        }
        return translations[self.language].get(text, text)

    def show_difficulty_selection(self):
        """Показує екран вибору складності гри."""
        self.clear_frame()

        title_label = tk.Label(self.main_frame, text=self.get_translation("Select Difficulty"), font=("Gabriola", 42, "bold"), bg="#f7eac6", fg="#6d4c41")
        title_label.pack(pady=40)

        easy_button = tk.Button(self.main_frame, text=self.get_translation("Easy Mode"), font=("Arial", 18, "bold"), bg="#c8e6c9", fg="black", command=lambda: self.start_game("easy"))
        easy_button.pack(pady=20)

        hard_button = tk.Button(self.main_frame, text=self.get_translation("Hard Mode"), font=("Arial", 18, "bold"), bg="#fff9c4", fg="black", command=lambda: self.start_game("hard"))
        hard_button.pack(pady=20)

        back_button = tk.Button(self.main_frame, text=self.get_translation("Back to Menu"), font=("Arial", 18, "bold"), bg="#ffccbc", fg="black", command=self.back_to_menu)
        back_button.pack(pady=20)

    def start_game(self, difficulty):
        """Запускає гру з обраною складністю."""
        self.root.destroy()
        menu_root = tk.Tk()
        game = Game(menu_root)
        game.ai.set_difficulty(difficulty)
        menu_root.mainloop()

    def show_rules(self):
        """Показує правила гри."""
        self.clear_frame()

        title_label = tk.Label(self.main_frame, text=self.get_translation("Rules of Hasami Shogi"), font=("Gabriola", 42, "bold"), bg="#f7eac6", fg="#6d4c41")
        title_label.pack(pady=20)

        rules_text = self.get_translation("Game Rules") + ":\n\n"
        if self.language == "ukrainian":
            rules_text += (
                "Хасамі-Шогі - це спрощена версія Шьогі, японських шахів.\n\n"
                "1. Мета гри:\n"
                "   Захопити всі фігури суперника або заблокувати їх, щоб вони не могли рухатись.\n\n"
                "2. Розстановка:\n"
                "   Кожен гравець починає з 9 фігур, розташованих у першому ряду.\n\n"
                "3. Рух фігур:\n"
                "   Фігури рухаються тільки вертикально або горизонтально на будь-яку кількість клітин.\n\n"
                "4. Захоплення фігур:\n"
                "   Фігура супротивника захоплюється, коли одна з ваших фігур переміщається на клітинку, яку займає фігура супротивника.\n\n"
                "5. Перемога:\n"
                "   Гравець виграє, якщо всі фігури супротивника будуть захоплені"
            )
        else:
            rules_text += (
                "Hasami Shogi is a simplified version of Shogi, a Japanese chess game.\n\n"
                "1. Objective:\n"
                "   Capture all of the opponent's pieces or block them so they can't move.\n\n"
                "2. Setup:\n"
                "   Each player starts with 9 pieces placed in the first row.\n\n"
                "3. Piece Movement:\n"
                "   Pieces move only vertically or horizontally across any number of squares.\n\n"
                "4. Capturing Pieces:\n"
                "   An opponent's piece is captured when one of your pieces moves to the square occupied by the opponent's piece.\n\n"
                "5. Victory:\n"
                "   A player wins by capturing all the opponent's pieces."
            )

        rules_label = tk.Label(self.main_frame, text=rules_text, font=("Arial", 18), bg="#f7eac6", fg="black", justify="left")
        rules_label.pack(pady=20)

        back_button = tk.Button(self.main_frame, text=self.get_translation("Back to Menu"), font=("Arial", 18, "bold"), bg="#ffccbc", fg="black", command=self.back_to_menu)
        back_button.pack(pady=20)

    def back_to_menu(self):
        """Повертає до головного меню."""
        self.create_main_menu()

    def clear_frame(self):
        """Очищає поточний фрейм."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def exit_game(self):
        """Виходить з гри."""
        self.root.quit()
