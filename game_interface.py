import tkinter as tk
import tkinter.font as tkFont
from game_logic import GameBoardIterator, GameBoard

class GameInterface:

    # The first object of each list will be used on empty spaces
    player_symbols = ["", "X", "O"]
    player_colors = ["white", "green", "red"]

    def __init__(self, master, game_board: GameBoard):
        self.game_board = game_board
        self.game_iterator: GameBoardIterator = game_board.board_iterator
        self.master = master
        master.title("Tic-Tac-Tron")

        self.btn_font = tkFont.Font(family="Arial", size=42, weight="bold")

        self.outer_frame = tk.Frame(master, bg = "white")
        self.outer_frame.pack(expand=True, anchor="center")

        self.board_frame = tk.Frame(self.outer_frame, bg="#555555")
        self.board_frame.pack(expand=True, anchor="center")

        # Using buttons to create the playing grid
        self.buttons = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text = self.player_symbols[0],
                    width = 4,
                    height = 2,
                    font = self.btn_font,
                    fg = self.player_colors[0],
                    activeforeground = self.player_colors[0],
                    bg = "white",
                    activebackground = "white",
                    relief = "flat",
                    highlightthickness = 0,
                    borderwidth = 0,
                    command = lambda r=row, c=col: self.perform_play(r, c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Restart option
        btn_restart = tk.Button(
            self.outer_frame,
            text = "Restart",
            width = 12,
            height = 1,
            font = self.btn_font,
            fg = "black",
            bg = "white",
            relief = "flat",
            command = self.restart
        )
        btn_restart.pack(anchor = "center", fill = "both", expand = True)

    def perform_play(self, row, col):
        if self.game_iterator.play(row, col, self.game_board):
            self.update_btn_info()
            self.finalize_if_over()
        if self.game_iterator.bot_play(self.game_board):
            self.update_btn_info()
            self.finalize_if_over()

    def restart(self):
        self.game_iterator.restart(self.game_board)
        self.board_frame.config(bg="#555555")
        self.update_btn_info()

    def update_btn_info(self):
        for row in range(3):
            for col in range(3):
                player_index = self.game_board.board_content[row][col]
                btn = self.buttons[row][col]
                try:
                    self.paint_normal_btn(btn, player_index)
                except IndexError:
                    btn["text"] = "?"
                    btn["fg"] = "grey"
                    btn["activeforeground"] = "grey"
    
    def finalize_if_over(self):
        if self.finalize_if_win():
            self.game_board.is_finished = True
            self.board_frame.config(bg="white")
            return True
        if self.finalize_if_tie():
            self.game_board.is_finished = True
            self.board_frame.config(bg="white")
            return True
        return False

    def finalize_if_win(self):
        winner = self.game_iterator.check_for_winner(self.game_board.board_content)
        if winner["type"] != "none":
            self.decorate_winner(winner)
            return True
        return False

    def finalize_if_tie(self):
        if self.game_iterator.check_if_full(self.game_board.board_content):
            self.decorate_tie()
            return True
        return False

    def decorate_winner(self, winner: dict):

        if winner["type"] == "row":
            row = winner["index"]
            for col in range(3):
                self.paint_winner_btn(self.buttons[row][col], winner["player"])

        elif winner["type"] == "column":
            col = winner["index"]
            for row in range(3):
                self.paint_winner_btn(self.buttons[row][col], winner["player"])

        elif winner["type"] == "diagonal" and winner["index"] == 0:
            for row in range(3):
                col = row
                self.paint_winner_btn(self.buttons[row][col], winner["player"])

        elif winner["type"] == "diagonal" and winner["index"] == 1:
            for row in range(3):
                col = 2 - row
                self.paint_winner_btn(self.buttons[row][col], winner["player"])

    def decorate_tie(self):
        for row in range(3):
            for col in range(3):
                btn = self.buttons[row][col]
                player_index = self.game_board.board_content[row][col]
                self.paint_tie_btn(btn, player_index)

    def paint_winner_btn(self, btn, player):
        btn["fg"] = self.player_colors[0]
        btn["bg"] = self.player_colors[player]
        btn["activeforeground"] = self.player_colors[0]
        btn["activebackground"] = self.player_colors[player]

    def paint_tie_btn(self, btn, player):
        btn["bg"] = "yellow"
        btn["activebackground"] = "yellow"

    def paint_normal_btn(self, btn, player):
        btn["text"] = self.player_symbols[player]
        btn["fg"] = self.player_colors[player]
        btn["bg"] = self.player_colors[0]
        btn["activeforeground"] = self.player_colors[player]
        btn["activebackground"] = self.player_colors[0]

class GameInterfaceStarter:

    @staticmethod
    def start(game_board):
        root = tk.Tk()
        root.configure(bg="white")
        window = GameInterface(root, game_board)

        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        scr_width = root.winfo_screenwidth()
        scr_height = root.winfo_screenheight()
        pos_x = (scr_width // 2) - (width // 2)
        pos_y = (scr_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        root.mainloop()