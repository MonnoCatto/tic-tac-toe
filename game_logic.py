from random import *
from debug_utils import MatrixPrinter as printer
import copy
from bots import GenericBot

class GameBoard:
    
    def __init__(self, board_iterator, board_content=None):
        if board_content == None:
            self.board_content = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
        else:
            self.board_content = board_content
        self.board_iterator = board_iterator
        self.is_finished = False
    
    def clear(self):
        for row in range(3):
            for col in range(3):
                self.board_content[row][col] = 0
        self.is_finished = False
    
    # For debugging
    def debug_print(self):
        printer.print(self.board_content)


class GameBoardIterator:

    def __init__(self, turn_handler):
        self.turn_handler = turn_handler

    def play(self, row, col, board: GameBoard):
        if not board.is_finished:
            try:
                if board.board_content[row][col] != 0:
                    return None
                
                # Since 0 represents an empty space, we add 1 to make player values be 1 and above
                board.board_content[row][col] = (self.turn_handler.get_turn() + 1)
                self.turn_handler.advance()

            except IndexError:
                print(f"ERROR caught in GameBoard.move(): Received value ({row, col}) is out of index range.")
            except TypeError:
                print(f"ERROR caught in GameBoard.move(): Received value ({row, col}) isn't an integer.")
            except Exception as e:
                print(e)
            return True
        else: 
            print("The game is finished.")
            return False

    def bot_play(self, board: GameBoard):
        if board.is_finished:
            return False
        row, col = self.bot.calculate_play(board.board_content)
        return self.play(row, col, board)
    
    def restart(self, board:GameBoard):
        board.clear()
        self.turn_handler.start_new()

    def check_for_winner(self, board):

        # Check for completed rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] != 0:
                winner = {
                    "player": board[row][0],
                    "type": "row",
                    "index": row
                }
                return winner
        
        # Check for completed columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != 0:
                winner = {
                    "player": board[0][col],
                    "type": "column",
                    "index": col
                }
                return winner
        
        # Check for the decreasing diagonal
        if board[0][0] == board[1][1] == board[2][2] != 0:
                winner = {
                    "player": board[1][1],
                    "type": "diagonal",
                    "index": 0
                }
                return winner
        
        # Check for the increasing diagonal
        if board[2][0] == board[1][1] == board[0][2] != 0:
                winner = {
                    "player": board[1][1],
                    "type": "diagonal",
                    "index": 1
                }
                return winner
        
        # Default return value
        winner = {
            "player": 0,
            "type": "none",
            "index": 0
        }
        return winner
    
    def check_if_full(self, board):
        for row in board:
            for space in row:
                if space == 0:
                    return False
        return True

    def add_bot(self, bot: GenericBot):
        self.bot = bot

class TurnHandler:
    
    def __init__(self, number_of_players=2, turn_offset=0):
        self.number_of_players = number_of_players
        self.first_turn = turn_offset % number_of_players
        self.turn = self.first_turn

    def advance(self):
        self.turn = (self.turn + 1) % self.number_of_players
    
    def get_turn(self):
        return self.turn
    
    def start_new(self):
        self.first_turn = (self.first_turn + 1) % self.number_of_players
        self.turn = self.first_turn

    def random(self):
        self.turn = random.randint(0, (self.number_of_players-1))
        return self.turn
    
    def random_restart(self):
        self.turn_offset = random.randint(0, (self.number_of_players-1))
        self.turn = self.turn_offset
        return self.current()
    
class GameHandler:

    def __init__(self, turn_handler: TurnHandler, board_iterator: GameBoardIterator):
        self.turn_handler = turn_handler
        self.board_iterator = board_iterator
        self.humans = 0
        self.bots = 0

    def handle_click(self, row, col):
        if not self.check_if_human_turn():
            return
        
    def check_if_human_turn(self):
        return self.turn_handler.get_turn() < self.humans