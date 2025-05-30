import copy
import random
from debug_utils import MatrixPrinter as printer

class GenericBot:

    def calculate_play(self, game_state):
        empty_indexes = []
        for row in range(3):
            for col in range(3):
                if game_state[row][col] != 0:
                    continue
                empty_indexes.append([row,col])
        return random.choice(empty_indexes)
        

class MiniMaxBot():

    def __init__(self, game_iterator):
        self.game_iterator = game_iterator
        self.number_of_players = game_iterator.turn_handler.number_of_players
        self.current_turn = 0

    def calculate_play(self, game_state):

        # Controlled random choice if the bot is playing first
        if self.count_empty_spaces(game_state) == 9:
            list_output = random.choices(
                population = [[1, 1], [0, 0], [0, 2], [2, 0], [2, 2]],
                weights = [0.5, 0.2, 0.2, 0.2, 0.2],
            )
            return list_output[0]
        
        print("Analysing options...\n\n")
        self.maximizing_player = self.game_iterator.turn_handler.get_turn() +1
        self.current_turn = self.game_iterator.turn_handler.get_turn()
        best_plays = []
        max_score = -9999
        for row in range(3):
            for col in range(3):
                if game_state[row][col] != 0:
                    continue
                self.current_turn = self.game_iterator.turn_handler.get_turn()
                proposed_state = copy.deepcopy(game_state)
                proposed_state[row][col] = self.maximizing_player
                proposed_state_score = self.minimax(proposed_state, self.count_empty_spaces(game_state), False, self.current_turn)
                printer.print(proposed_state)
                print(f"Proposed value: {proposed_state_score}\n\n")
                if proposed_state_score > max_score:
                    max_score = proposed_state_score
                    best_plays = [[row, col]]
                elif proposed_state_score == max_score:
                    best_plays.append([row,col])
        return random.choice(best_plays)
                
    def minimax(self, game_state, depth, maximizing_player_turn, current_turn):
        if depth == 0 or self.is_state_finished(game_state):
            return self.evaluate(game_state)
        next_turn = ((current_turn +1) % self.number_of_players)
        if maximizing_player_turn:
            max_eval = -9999
            for child in self.generate_children(game_state, next_turn):
                current_eval = self.minimax(child, depth-1, False, next_turn)
                max_eval = max(max_eval, current_eval)
            return max_eval
        
        else:
            min_eval = 9999
            for child in self.generate_children(game_state, next_turn):
                current_eval = self.minimax(child, depth-1, True, next_turn)
                min_eval = min(min_eval, current_eval)
            return min_eval
    
    def generate_children(self, game_state, current_turn):
        current_player = current_turn +1
        children = []
        for row in range(3):
            for col in range(3):
                if game_state[row][col] != 0:
                    continue
                child = copy.deepcopy(game_state)
                child[row][col] = current_player
                children.append(child)
        return children

    def evaluate(self, game_state):
        winner = self.game_iterator.check_for_winner(game_state)
        empty_spaces = self.count_empty_spaces(game_state)

        if winner["player"] == self.maximizing_player:
            return (1 + empty_spaces) # More empty spaces == faster win == better
        elif winner["player"] == 0:
            return 0
        else:
            return (-1 - empty_spaces) # More empty spaces == faster loss == worse
        
    def is_state_finished(self, game_state):
        if self.game_iterator.check_for_winner(game_state)["type"] != "none":
            return True
        if self.game_iterator.check_if_full(game_state):
            return True
        return False

    def count_empty_spaces(self, game_state):
        empty_spaces = 0
        for row in range(3):
            for col in range(3):
                if game_state[row][col] == 0:
                    empty_spaces += 1
        return empty_spaces