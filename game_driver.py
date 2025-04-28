from game_logic import *
from game_interface import GameInterfaceStarter as ui
from bots import MiniMaxBot

def main():
    
    turn_handler = TurnHandler()
    board_iterator = GameIterator(turn_handler)
    game = GameBoard(turn_handler, board_iterator)
    minimax = MiniMaxBot(board_iterator)
    board_iterator.add_bot(minimax)
    ui.start(game)

if __name__=="__main__":
    main()