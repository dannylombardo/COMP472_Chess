import math
import copy
import time
import argparse
import sys, traceback

NumOfMoves = 0

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()
        self.move_counter = 0

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
        start, end = move  # Define start and end here
        captured_piece = self.captured_piece(game_state, end)

        # ----------- Scenario 1: Moves a piece from one location to the other as well as when a piece is removed from the game(for general cases ONLY) -----------

        moveCodeLetter = 'A'                    # Initialized to random letter (used for the logger notation)
        moveCodeNumber = '1'                    # Initialized to random number (used for the logger notation)
        eliminated = False                      # Initialized to a piece not being eliminated
        pawnToQueen = False                     # Initialized switch that checks if pawn has become queen

        start_row, start_col = start            # the x position of the coordinate goes to start_row and the y position goes start_col
        end_row, end_col = end                  # this step isn't needed but just for easier readability
        
        pieceEliminated = game_state["board"][0][4]                     # random spot (just to initialize)

        piece = game_state["board"][start_row][start_col]               # copies the piece that is being moved
        game_state["board"][start_row][start_col] = '.'                 # replaces that initial spot with a '.'

        if game_state["board"][end_row][end_col] != '.':
            pieceEliminated = game_state["board"][end_row][end_col]     # keeps track of the eliminated piece
            eliminated = True                                           # turns on the switch (that piece has been eliminated in this turn)

        game_state["board"][end_row][end_col] = piece                   # updates the piece at the end location


        if end_row == 0:
            moveCodeNumber = '5'              # Initializing the code for the number to be used in the logger (since they dont have the same numbering and lettering)
        elif end_row == 1:
            moveCodeNumber = '4'
        elif end_row == 2:
            moveCodeNumber = '3'
        elif end_row == 3:
            moveCodeNumber = '2'
        elif end_row == 4:
            moveCodeNumber = '1'

        if end_col == 0:
            moveCodeLetter = 'A'              # Initializing the code for the letter to be used in the logger (since they dont have the same numbering and lettering)
        elif end_col == 1:
            moveCodeLetter = 'B'
        elif end_col == 2:
            moveCodeLetter = 'C'
        elif end_col == 3:
            moveCodeLetter = 'D'
        elif end_col == 4:
            moveCodeLetter = 'E'
        

        if game_state["turn"] == "white":                               # switches the turn of the player
            game_state["turn"] = "black"
        else:
            game_state["turn"] = "white"
        

        # ----------- Scenario 2: If a white pawn moves to the last row, it becomes a white queen -----------

        if game_state["board"][0][0] == 'wp':
            game_state["board"][0][0] = 'wQ'                # becomes a queen (for white)
            pawnToQueen = True

        elif game_state["board"][0][1] == 'wp':
            game_state["board"][0][1] = 'wQ'                # becomes a queen (for white)
            pawnToQueen = True

        elif game_state["board"][0][2] == 'wp':
            game_state["board"][0][2] = 'wQ'                # becomes a queen (for white)
            pawnToQueen = True

        elif game_state["board"][0][3] == 'wp':
            game_state["board"][0][3] = 'wQ'                # becomes a queen (for white)
            pawnToQueen = True

        elif game_state["board"][0][4] == 'wp':
            game_state["board"][0][4] = 'wQ'                # becomes a queen (for white)
            pawnToQueen = True

        
        # ----------- Scenario 3: If a black pawn moves to the last row, it becomes a black queen -----------


        if game_state["board"][4][0] == 'bp':
            game_state["board"][4][0] = 'bQ'                # becomes a queen (for black)
            pawnToQueen = True

        elif game_state["board"][4][1] == 'bp':
            game_state["board"][4][1] = 'bQ'                # becomes a queen (for black)
            pawnToQueen = True

        elif game_state["board"][4][2] == 'bp':
            game_state["board"][4][2] = 'bQ'                # becomes a queen (for black)
            pawnToQueen = True

        elif game_state["board"][4][3] == 'bp':
            game_state["board"][4][3] = 'bQ'                # becomes a queen (for black)
            pawnToQueen = True

        elif game_state["board"][4][4] == 'bp':
            game_state["board"][4][4] = 'bQ'                # becomes a queen (for black)
            pawnToQueen = True


        # ----------- Scenario 4: If the white king is eliminated -----------

        if pieceEliminated == 'wK':
            with open("COMP472_Project.txt", "a") as f:
                f.write(piece + ' has moved to ' + (moveCodeLetter + moveCodeNumber) + ' and the white king has been eliminated ' + '\n' + 'GAME OVER: BLACK WINS \n')
            print("Black wins!")
            sys.exit(0)

        # ----------- Scenario 5: If the black king is eliminated -----------

        if pieceEliminated == 'bK':
            with open("COMP472_Project.txt", "a") as f:
                f.write(piece + ' has moved to ' + (moveCodeLetter + moveCodeNumber) + ' and the black king has been eliminated ' + '\n' + 'GAME OVER: WHITE WINS \n')
            print("White wins!")
            sys.exit(0)


        # ----------- Game / Move logger (Tracks the moves in the game) -----------

        
        if eliminated == True:
            with open("COMP472_Project.txt", "a") as f:
                f.write(piece + ' has moved to ' + (moveCodeLetter + moveCodeNumber) + ' and ' + pieceEliminated + ' is now eliminated from the game \n')
        elif pawnToQueen == False:
            with open("COMP472_Project.txt", "a") as f:
                f.write(piece + ' has moved to ' + (moveCodeLetter + moveCodeNumber) + '\n')
        else:
            with open("COMP472_Project.txt", "a") as f:
                f.write(piece + ' has moved to ' + (moveCodeLetter + moveCodeNumber) + ' and it is now become a queen' + '\n')

        pawnToQueen = False                                 # reset the pawnToQueen to false so that it can be checked for in the future moves
        eliminated = False                                  # reset the eliminated to false so that it can check for the future moves

        if captured_piece != '.':
            self.move_counter = 0
            NumOfMoves = self.move_counter
            if captured_piece in ('bK', 'wK'):
                print(f"{game_state['turn']} wins!")
                exit(1)
        else:
            self.move_counter += 1
            NumOfMoves = self.move_counter

        if self.move_counter >= 13:
            print("Game is a draw!")
            exit(1)

        # ----------- Scenario 6: Detect Draw -----------

        if NumOfMoves >= 10:
            with open("COMP472_Project.txt", "a") as f:
                f.write('GAME OVER: DRAW \n')
            print("No one won... It's a draw!")
            sys.exit(0)


        return game_state
        
    def captured_piece(self, game_state, end):
        end_row, end_col = end
        piece = game_state["board"][end_row][end_col]
        return piece if piece != '.' else '.'
    
    # Check if the king is on the board
    def king_exists(self, game_state):
        for row in game_state["board"]:
            if "wK" in row or "bK" in row:
                return True
            return False

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
        print("Welcome to Mini Chess!")

        print("Choose the mode:"
              "\n1. Player vs Player"
              "\n2. Player vs AI"
              "\n3. AI vs AI")
        mode = input("Enter the mode number: ")
        if mode == '1':
            print("Player vs Player mode selected.")
        elif mode == '2':
            print("AI CPU not implemented yet. Exiting game.")
            exit(1)
        elif mode == '3':
            print("AI CPU not implemented yet. Exiting game.")
            exit(1)
        else:
            print("Invalid mode. Exiting game.")
            exit(1)

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