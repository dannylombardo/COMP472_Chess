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
            print(str(6 - i) + "  " + ' '.join(piece.rjust(3) for piece in row))
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
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]

        if piece == '.': # No piece to move
            return False

        piece_color = 'white' if piece[0] == 'w' else 'black'

        if piece_color != game_state["turn"]: # Check if it's the correct turn
            return False

        valid_moves = self.valid_moves(game_state)

        return move in valid_moves

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """

    def valid_moves(self, game_state):
        moves = []
        board = game_state["board"]
        turn = game_state["turn"]

        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece != '.' and ((turn == "white" and piece[0] == 'w') or (turn == "black" and piece[0] == 'b')):
                    moves.extend(self.get_piece_moves(board, row, col, piece))

        return moves

    def get_piece_moves(self, board, row, col, piece):
        piece_type = piece[1]
        if piece_type == 'K':
            return self.king_moves(board, row, col)
        elif piece_type == 'Q':
            return self.queen_moves(board, row, col)
        elif piece_type == 'B':
            return self.bishop_moves(board, row, col)
        elif piece_type == 'N':
            return self.knight_moves(board, row, col)
        elif piece_type == 'p':
            return self.pawn_moves(board, row, col, piece[0])
        return []

    def king_moves(self, board, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return self.get_moves_in_directions(board, row, col, directions, limit=1)

    def queen_moves(self, board, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return self.get_moves_in_directions(board, row, col, directions)

    def bishop_moves(self, board, row, col):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.get_moves_in_directions(board, row, col, directions)

    def knight_moves(self, board, row, col):
        moves = []
        possible_jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in possible_jumps:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 5 and 0 <= new_col < 5 and (
                    board[new_row][new_col] == '.' or board[new_row][new_col][0] != board[row][col][0]):
                moves.append(((row, col), (new_row, new_col)))
        return moves

    def pawn_moves(self, board, row, col, color):
        moves = []
        direction = -1 if color == 'w' else 1
        new_row = row + direction

        if 0 <= new_row < 5:
            # Forward move (only if the destination is empty)
            if board[new_row][col] == '.':
                moves.append(((row, col), (new_row, col)))

            # Capture diagonally
            for new_col in [col - 1, col + 1]:
                if 0 <= new_col < 5 and board[new_row][new_col] != '.' and board[new_row][new_col][0] != color:
                    moves.append(((row, col), (new_row, new_col)))

        return moves

    def get_moves_in_directions(self, board, row, col, directions, limit=5):
        moves = []
        piece_color = board[row][col][0]
        for dr, dc in directions:
            for step in range(1, limit + 1):
                new_row, new_col = row + dr * step, col + dc * step
                if 0 <= new_row < 5 and 0 <= new_col < 5:
                    if board[new_row][new_col] == '.':
                        moves.append(((row, col), (new_row, new_col)))
                    elif board[new_row][new_col][0] != piece_color:
                        moves.append(((row, col), (new_row, new_col)))
                        break  # Stop moving in this direction if capturing an enemy piece
                    else:
                        break  # Stop if blocked by own piece
                else:
                    break  # Stop if out of bounds
        return moves

    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """

    def make_move(self, game_state, move):
        start = move[0]
        end = move[1]
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

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