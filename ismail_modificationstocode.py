import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    """
    Check if the move is valid    
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
    def is_valid_move(self, game_state, move):
        # Check if move is in list of valid moves
        return True

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_moves(self, game_state):
        # Return a list of all the valid moves.
        # Implement basic move validation
        # Check for out-of-bounds, correct turn, move legality, etc
        return

    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):

        # ----------- Scenario 1: Moves a piece from one location to the other (for general cases ONLY) -----------

        start = move[0]                         # the zero index will always the begining coordinates of the move (ex. (6, 4))
        end = move[1]                           # the first index of move will contain the end coordinates of the move (ex. (5, 4))

        start_row, start_col = start            # the x position of the coordinate goes to start_row and the y position goes start_col
        end_row, end_col = end                  # this step isn't needed but just for easier readability
        
        piece = game_state["board"][start_row][start_col]               # copies the piece that is being moved
        game_state["board"][start_row][start_col] = '.'                 # replaces that initial spot with a '.'
        game_state["board"][end_row][end_col] = piece                   # updates the piece at the end location


        if game_state["turn"] == "white":                               # switches the turn of the player
            game_state["turn"] = "black"
        else:
            game_state["turn"] = "white"
        

        # ----------- Scenario 2: If a white pawn moves to the last row, it becomes a white queen -----------

        if game_state["board"][0][0] == 'wp':
            game_state["board"][0][0] = 'wQ'                # becomes a queen (for white)

        elif game_state["board"][0][1] == 'wp':
            game_state["board"][0][1] = 'wQ'                # becomes a queen (for white)

        elif game_state["board"][0][2] == 'wp':
            game_state["board"][0][2] = 'wQ'                # becomes a queen (for white)

        elif game_state["board"][0][3] == 'wp':
            game_state["board"][0][3] = 'wQ'                # becomes a queen (for white)

        elif game_state["board"][0][4] == 'wp':
            game_state["board"][0][4] = 'wQ'                # becomes a queen (for white)

        
        # ----------- Scenario 3: If a black pawn moves to the last row, it becomes a black queen -----------


        if game_state["board"][4][0] == 'bp':
            game_state["board"][4][0] = 'bQ'                # becomes a queen (for black)

        elif game_state["board"][4][1] == 'bp':
            game_state["board"][4][1] = 'bQ'                # becomes a queen (for black)

        elif game_state["board"][4][2] == 'bp':
            game_state["board"][4][2] = 'bQ'                # becomes a queen (for black)

        elif game_state["board"][4][3] == 'bp':
            game_state["board"][4][3] = 'bQ'                # becomes a queen (for black)

        elif game_state["board"][4][4] == 'bp':
            game_state["board"][4][4] = 'bQ'                # becomes a queen (for black)


        

        return game_state

    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        while True:
            self.display_board(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue

            self.make_move(self.current_game_state, move)

if __name__ == "__main__":
    game = MiniChess()
    game.play()
