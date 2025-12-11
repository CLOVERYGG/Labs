
import tkinter as tk
from tkinter import messagebox
import random
import math

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Стратегические Крестики-Нолики")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")  # Темно-синий фон

        # Цвета и стили
        self.primary_color = "#3498db"  # Яркий синий (O)
        self.secondary_color = "#e74c3c" # Красный (X)
        self.button_bg = "#ecf0f1"      # Светло-серый
        self.hover_bg = "#bdc3c7"       # Более темный серый для наведения
        self.text_color = "#2c3e50"
        # win_color удалён - больше не используем подсветку клеток

        self.board = [''] * 9
        self.current_player = 'X'
        self.player_symbol = ''
        self.ai_symbol = ''
        self.game_active = False
        self.scores = {'X': 0, 'O': 0}
        self.moves_count = {'X': 0, 'O': 0}

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_screen()
        container = tk.Frame(self.root, bg="#2c3e50")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Стратегические", font=("Helvetica Neue", 30, "bold"),
                 fg="#ffffff", bg="#2c3e50").pack(pady=(30, 10))
        tk.Label(container, text="Крестики-Нолики", font=("Helvetica Neue", 30, "bold"),
                 fg=self.primary_color, bg="#2c3e50").pack(pady=(0, 40))

        tk.Label(container, text="Выберите свою роль:", font=("Helvetica Neue", 14, "italic"),
                 fg="#ecf0f1", bg="#2c3e50").pack(pady=10)

        btn_x = tk.Button(container, text="Быть Крестиком (X)", font=("Helvetica Neue", 12, "bold"),
                          width=25, bg="#f1c40f", fg="#2c3e50",
                          pady=12, relief="flat", bd=0,
                          activebackground="#e67e22", activeforeground="#ffffff",
                          command=lambda: self.start_game('X'))
        btn_x.pack(pady=15)
        btn_x.bind("<Enter>", lambda e: e.widget.config(bg="#e67e22", fg="#ffffff"))
        btn_x.bind("<Leave>", lambda e: e.widget.config(bg="#f1c40f", fg="#2c3e50"))

        btn_o = tk.Button(container, text="Быть Ноликом (O)", font=("Helvetica Neue", 12, "bold"),
                          width=25, bg="#2980b9", fg="#ffffff",
                          pady=12, relief="flat", bd=0,
                          activebackground="#3498db", activeforeground="#ffffff",
                          command=lambda: self.start_game('O'))
        btn_o.pack(pady=15)
        btn_o.bind("<Enter>", lambda e: e.widget.config(bg="#3498db", fg="#ffffff"))
        btn_o.bind("<Leave>", lambda e: e.widget.config(bg="#2980b9", fg="#ffffff"))

    def start_game(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = 'O' if symbol == 'X' else 'X'
        self.game_active = True
        self.board = [''] * 9
        self.moves_count = {'X': 0, 'O': 0}
        self.current_player = 'X' # Крестики всегда ходят первыми
        self.clear_screen()
        self.setup_game_ui()
        if self.current_player == self.ai_symbol:
            self.root.after(500, self.ai_move)

    def setup_game_ui(self):
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        board_frame = tk.Frame(main_frame, bg="#34495e", bd=3, relief="groove")
        board_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=("Poppins", 40, "bold"),
                                width=4, height=2, bg=self.button_bg, fg=self.text_color,
                                relief="flat", bd=0,
                                command=lambda i=i, j=j: self.player_move(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg=self.hover_bg))
                btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg=self.button_bg))
                self.buttons.append(btn)

        info_frame = tk.Frame(main_frame, bg="#2c3e50", width=250)
        info_frame.grid(row=0, column=1, sticky="nse", padx=20)
        info_frame.grid_propagate(False)

        tk.Label(info_frame, text="Ваша роль:", font=("Poppins", 14, "bold"),
                 fg="#ffffff", bg="#2c3e50").pack(pady=(15, 5))
        player_role_color = self.secondary_color if self.player_symbol == 'X' else self.primary_color
        tk.Label(info_frame, text=f"{self.player_symbol}",
                 font=("Poppins", 30, "bold"),
                 fg=player_role_color, bg="#2c3e50").pack(pady=(0, 20))

        self.turn_label = tk.Label(info_frame, text="Ход: X",
                                   font=("Poppins", 18, "bold"),
                                   fg="#ffffff", bg="#2c3e50")
        self.turn_label.pack(pady=20)

        self.moves_label = tk.Label(info_frame, text="Ходы:\nX: 0\nO: 0",
                                    font=("Poppins", 12),
                                    fg="#bdc3c7", bg="#2c3e50", justify="left")
        self.moves_label.pack(pady=25)

        self.score_label = tk.Label(info_frame, text="Счет:\nX: 0 | O: 0",
                                    font=("Poppins", 12, "bold"),
                                    fg="#ecf0f1", bg="#2c3e50")
        self.score_label.pack(pady=(25, 40))

        btn_reset = tk.Button(info_frame, text="🔄 Новая партия", font=("Poppins", 11, "bold"),
                              bg="#3498db", fg="#ffffff",
                              pady=10, relief="flat", bd=0,
                              activebackground="#2980b9", activeforeground="#ffffff",
                              command=lambda: self.start_game(self.player_symbol))
        btn_reset.pack(fill="x", pady=8)
        btn_reset.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
        btn_reset.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))

        btn_menu = tk.Button(info_frame, text="🏠 Главное меню", font=("Poppins", 11, "bold"),
                             bg="#95a5a6", fg="#ffffff",
                             pady=10, relief="flat", bd=0,
                             activebackground="#7f8c8d", activeforeground="#ffffff",
                             command=self.create_start_screen)
        btn_menu.pack(fill="x", pady=8)
        btn_menu.bind("<Enter>", lambda e: e.widget.config(bg="#7f8c8d"))
        btn_menu.bind("<Leave>", lambda e: e.widget.config(bg="#95a5a6"))

        self.score_label.config(text=f"Счет:\nX: {self.scores['X']} | O: {self.scores['O']}")
        self.update_moves_display()

    def player_move(self, row, col):
        if not self.game_active or self.current_player != self.player_symbol:
            return
        index = row * 3 + col
        if self.board[index] == '':
            self.update_board(index, self.player_symbol)
            self.moves_count[self.player_symbol] += 1
            self.update_moves_display()

            if self.check_winner(self.player_symbol):
                self.end_game(self.player_symbol)
            elif self.check_draw():
                self.end_game(None)
            else:
                self.current_player = self.ai_symbol
                self.turn_label.config(text=f"Ход: {self.ai_symbol}", fg=self.primary_color if self.ai_symbol == 'O' else self.secondary_color)
                self.root.after(600, self.ai_move)

    def update_board(self, index, symbol):
        self.board[index] = symbol
        btn = self.buttons[index]
        btn.config(text=symbol,
                   fg=self.secondary_color if symbol == 'X' else self.primary_color,
                   bg=self.button_bg,
                   state=tk.DISABLED) # Делаем кнопку неактивной после хода
        btn.unbind("<Enter>")
        btn.unbind("<Leave>")

    def ai_move(self):
        if not self.game_active:
            return

        best_score = -math.inf
        best_move = -1
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = self.ai_symbol
                score = self.minimax(self.board, False)
                self.board[i] = '' # Отменяем ход

                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move != -1:
            self.update_board(best_move, self.ai_symbol)
            self.moves_count[self.ai_symbol] += 1
            self.update_moves_display()

            if self.check_winner(self.ai_symbol):
                self.end_game(self.ai_symbol)
            elif self.check_draw():
                self.end_game(None)
            else:
                self.current_player = self.player_symbol
                self.turn_label.config(text=f"Ход: {self.player_symbol}", fg=self.secondary_color if self.player_symbol == 'X' else self.primary_color)

    def minimax(self, board, is_maximizing):
        if self.check_winner(self.ai_symbol):
            return 10
        if self.check_winner(self.player_symbol):
            return -10
        if self.check_draw():
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = self.ai_symbol
                    eval = self.minimax(board, False)
                    board[i] = ''
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = self.player_symbol
                    eval = self.minimax(board, True)
                    board[i] = ''
                    min_eval = min(min_eval, eval)
            return min_eval

    def check_winner(self, p):
        win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for cond in win_conditions:
            if self.board[cond[0]] == self.board[cond[1]] == self.board[cond[2]] == p:
                # Ранее здесь подсвечивались клетки. Теперь ничего не меняем во внешнем виде.
                return True
        return False

    def check_draw(self):
        return '' not in self.board

    def end_game(self, winner):
        self.game_active = False
        msg = ""
        title = ""

        if winner:
            self.scores[winner] += 1
            if winner == self.player_symbol:
                msg = "Поздравляем! Вы одержали верх!"
                title = "Триумф!"
            else:
                msg = "Неудача! Искусственный интеллект оказался хитрее."
                title = "Урок усвоен."
        else:
            msg = "Поле заполнено. Результат - ничья!"
            title = "Мирное соглашение."

        # Никаких изменений фона кнопок - только сообщение и обновление счёта
        self.root.after(100, lambda: messagebox.showinfo(title, msg))
        self.root.after(120, self.update_score_display)

    def update_moves_display(self):
        self.moves_label.config(text=f"Ходы:\nX: {self.moves_count['X']}\nO: {self.moves_count['O']}")

    def update_score_display(self):
        self.score_label.config(text=f"Счет:\nX: {self.scores['X']} | O: {self.scores['O']}")

    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeAI(root)
    root.mainloop()
