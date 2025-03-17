import math
import copy
import time
import argparse
import sys, traceback

NumOfMoves = 0
WhiteMoveCounter = 0
BlackMoveCounter = 0
TIME_LIMIT = 5  # Time limit in seconds for the AI to make a move

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()
        self.new_game_state = self.init_board()

        self.move_counter = 0
        self.ai_color = None

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

    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6 - i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    def is_valid_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]

        if piece == '.':  # No piece to move
            return False

        piece_color = 'white' if piece[0] == 'w' else 'black'

        if piece_color != game_state["turn"]:  # Check if it's the correct turn
            return False

        valid_moves = self.valid_moves(game_state)

        return move in valid_moves

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

    def make_move(self, game_state, move, log_move=True, simulation=False):
        
        print(f"Making move: {move}")

        global WhiteMoveCounter
        global BlackMoveCounter
        global NumOfMoves

        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        captured_piece = self.captured_piece(game_state, end)

        # Check if the move is valid
        if not self.is_valid_move(game_state, move):
            print("Invalid move. Try again.")
            return game_state

        if piece == '.':
            print("ERROR: Trying to move an empty square!")
            return game_state  # Prevent breaking the board


        # Save the original position of the kings before moving
        king_positions = {"wK": None, "bK": None}
        for r in range(5):
            for c in range(5):
                if game_state["board"][r][c] in king_positions:
                    king_positions[game_state["board"][r][c]] = (r, c)


        # Move the piece
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece

        pawn_to_queen = self.handle_pawn_promotion(game_state)

        # Prevent simulation moves from affecting real game state
        if not simulation:
            # Check for game-ending conditions
            piece_eliminated = self.check_game_end_conditions(game_state, piece, end_row, end_col)

            if log_move:
                self.log_move(piece, end_row, end_col, captured_piece, pawn_to_queen, piece_eliminated)

            # Update move counters and check for draw
            self.update_move_counters(captured_piece)
            self.check_for_draw()

        is_sim = simulation
        # Ensure a king wasn't falsely removed
        if not self.king_exists(game_state, is_sim):
            print("ERROR: The King disappeared after the move! Undoing move.")
            game_state["board"][start_row][start_col] = piece  # Undo move
            game_state["board"][end_row][end_col] = '.'  # Restore board state
            return game_state  # Return unchanged game state

        # Switch turns
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state

    def handle_pawn_promotion(self, game_state):
        pawn_to_queen = False
        for col in range(5):
            if game_state["board"][0][col] == 'wp':
                game_state["board"][0][col] = 'wQ'
                pawn_to_queen = True
            elif game_state["board"][4][col] == 'bp':
                game_state["board"][4][col] = 'bQ'
                pawn_to_queen = True
        return pawn_to_queen

    def check_game_end_conditions(self, game_state, piece, end_row, end_col):
        white_king_exists = False
        black_king_exists = False

        # Check if the kings are still on the board
        for row in game_state["board"]:
            for piece in row:
                if piece == 'wK':
                    white_king_exists = True
                elif piece == 'bK':
                    black_king_exists = True

        if not white_king_exists:
            self.end_game("Black wins!", "BLACK WINS")
        elif not black_king_exists:
            self.end_game("White wins!", "WHITE WINS")

        return game_state["board"][end_row][end_col]  # Return the piece that was eliminated (if any)    
    
    def end_game(self, message, log_message):
        with open("COMP472_Project.txt", "a") as f:
            f.write(f'GAME OVER: {log_message} \n')
        print(message)
        sys.exit(0)

    def log_move(self, piece, end_row, end_col, captured_piece, pawn_to_queen, piece_eliminated):
        move_code_letter = chr(ord('A') + end_col)
        move_code_number = str(5 - end_row)
        with open("COMP472_Project.txt", "a") as f:
            if captured_piece != '.':
                f.write(f'{piece} has moved to {move_code_letter}{move_code_number} and {piece_eliminated} is now eliminated from the game \n')
            elif pawn_to_queen:
                f.write(f'{piece} has moved to {move_code_letter}{move_code_number} and it has become a queen \n')
            else:
                f.write(f'{piece} has moved to {move_code_letter}{move_code_number} \n')

    def update_move_counters(self, captured_piece):
        global WhiteMoveCounter
        global BlackMoveCounter
        global NumOfMoves

        if captured_piece != '.':
            self.move_counter = 0
        else:
            self.move_counter += 1

        NumOfMoves = self.move_counter

        if self.current_game_state["turn"] == "white":
            WhiteMoveCounter += 1
            with open("COMP472_Project.txt", "a") as f:
                f.write(f"White Move Counter: {WhiteMoveCounter}\n")
        else:
            BlackMoveCounter += 1
            with open("COMP472_Project.txt", "a") as f:
                f.write(f"Black Move Counter: {BlackMoveCounter}\n")

    def check_for_draw(self):
        if self.move_counter >= 10:
            with open("COMP472_Project.txt", "a") as f:
                f.write('GAME OVER: DRAW \n')
            print("No one won... It's a draw!")
            sys.exit(0)

    def captured_piece(self, game_state, end):
        end_row, end_col = end
        piece = game_state["board"][end_row][end_col]
        return piece if piece != '.' else '.'

    # Check if the king is on the board
    def king_exists(self, game_state, simulation=False):

        white_king = False
        black_king = False

        for row in game_state["board"]:
            for piece in row:
                if piece == "wK":
                    white_king = True
                elif piece == "bK":
                    black_king = True

        if simulation:
            return white_king and black_king  # Just return status, don't exit game

        if not white_king:
            self.end_game("Black wins!", "BLACK WINS")
        elif not black_king:
            self.end_game("White wins!", "WHITE WINS")

        return white_king and black_king

    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5 - int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5 - int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

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
            print("Player vs AI mode selected.")
        elif mode == '3':
            print("AI vs AI mode selected.")
        else:
            print("Invalid mode. Exiting game.")
            exit(1)

        if mode == '2' or mode == '3':
            print("Which color should player 1 be? (w/b): ")
            player1_color = input().strip().lower()

            if player1_color == 'w':
                print("Player 1 is white and starts first.")
                self.current_game_state["turn"] = 'white'
                self.ai_color = "black"  
            elif player1_color == 'b':
                print("Player 1 is black and starts second (after first AI).")
                self.current_game_state["turn"] = 'white'
                self.ai_color = "white"  
            else:
                print("Invalid color. Exiting game.")
                exit(1)

            print("Do you want minimax or alpha-beta pruning? (m/a): ")
            algorithm = input().strip().lower()
            if algorithm not in ['m', 'a']:
                print("Invalid algorithm. Exiting game.")
                exit(1)

            print("Select timeout time for the AI: ")
            global TIME_LIMIT
            TIME_LIMIT = int(input().strip())

            print("Select max number of turns (in total): ")
            max_turns = int(input().strip())

        print("Enter 'exit' to quit the game.")

        while True:
            self.display_board(self.current_game_state)

            if self.current_game_state['turn'] == self.ai_color:  # AI's Turn
                print("AI is thinking...")
                start_time = time.time()
                best_eval, move = self.use_minimax(self.current_game_state, alpha=-math.inf, beta=math.inf, maximizing_player=(self.ai_color == 'white'), start_time=start_time)

                if move is None:
                    print(f"AI ({self.ai_color}) has no valid moves. It loses!")
                    exit(1)

                print(f"AI ({self.ai_color}) move: {move}")

                self.current_game_state = self.make_move(self.current_game_state, move, simulation=False)

            else:  # Human Player's Turn
                move = input(f"{self.current_game_state['turn'].capitalize()} to move: ").strip()
                if move.lower() == 'exit':
                    print("Game exited.")
                    exit(1)

                move = self.parse_input(move)
                if not move or not self.is_valid_move(self.current_game_state, move):
                    print("Invalid move. Try again.")
                    continue

                self.current_game_state = self.make_move(self.current_game_state, move, simulation=False)

            if(mode == 2 or mode == 3):
                global NumOfMoves
                NumOfMoves += 1
                if NumOfMoves >= max_turns:
                    print("Max number of turns reached. Exiting game.")
                    exit(1)
                                
    def use_minimax(self, game_state, alpha, beta, maximizing_player, start_time):
        print(f"Time1 Elapsed: {time.time() - start_time:.2f}s")
        print(f"Board Evaluation1: {self.evaluate_board(game_state)}")
        print(f"AI's available moves: {self.valid_moves(game_state)}")

        print(f"AI's color: {self.ai_color}")
        print(f"AI is maximizing: {maximizing_player}")
        print(f"Board Evaluation: {self.evaluate_board(game_state)}")

        
        best_move = None
        best_eval = -math.inf if maximizing_player else math.inf
        depth = 1

        while depth <= 50:  # Limit depth to prevent infinite recursion
            print(f"Minimax running at depth {depth}")
            current_eval, current_move = self.minimax(game_state, depth, alpha, beta, maximizing_player, start_time)

            if current_move is not None:
                best_eval = current_eval
                best_move = current_move

            # Stop the search if the time limit is reached
            if (time.time() - start_time) >= TIME_LIMIT:
                break

            depth += 1


        print(f"Time2 Elapsed: {time.time() - start_time:.2f}s")
        print(f"Board Evaluation2: {self.evaluate_board(game_state)}")
        print(f"Best move found: {best_move}")

        print(f"AI's color: {self.ai_color}")
        print(f"AI is maximizing: {maximizing_player}")
        print(f"Best move at depth {depth}: {best_move}")
        print(f"Board Evaluation: {self.evaluate_board(game_state)}")
        
        return best_eval, best_move

    def minimax(self, game_state, depth, alpha, beta, maximizing_player, start_time):

        print(f"Minimax Depth: {depth}, Maximizing: {maximizing_player}")
        print(f"Board Evaluation1: {self.evaluate_board(game_state)}")           
        print(f"Time1 Elapsed: {time.time() - start_time:.2f}s")
        print(f"Minimax Depth: {depth}, Maximizing: {maximizing_player}")

        if depth == 0 or not self.king_exists(game_state, simulation=True) or (time.time() - start_time) >= TIME_LIMIT:
            return self.evaluate_board(game_state), None

        # Initialize the best move and evaluation variables
        best_move = None
        best_eval = -math.inf if maximizing_player else math.inf

        moves = self.valid_moves(game_state)
        print(f"Valid moves at depth {depth}: {moves}")

        
        # testing and trying to sort based on eval
        def move_evaluation(move):
            test_game_state = copy.deepcopy(game_state)
            test_game_state = self.make_move(test_game_state, move, log_move=False, simulation=True)
            return self.evaluate_board(test_game_state)

        moves.sort(key=move_evaluation, reverse=maximizing_player)  #Sort in best order

        for move in moves:
            if (time.time() - start_time) >= TIME_LIMIT - 0.2:
                break

            # Create a new game state by making the move
            new_game_state = copy.deepcopy(game_state)

            print(f"NEW BOARD Before move: ")
            self.display_board(new_game_state)

            new_game_state = self.make_move(new_game_state, move, log_move=False, simulation=True)

            print(f"NEW BOARD After move: ")
            self.display_board(new_game_state)

            # Recursively call minimax with the new game state and updated parameters
            eval, _ = self.minimax(new_game_state, depth - 1, alpha, beta, not maximizing_player, start_time)

            # Update the best move and evaluation based on the maximizing or minimizing player
            if maximizing_player:
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
            else:
                if eval < best_eval:
                    best_eval = eval
                    best_move = move
                beta = min(beta, eval)

        print(f"Board Evaluation2: {self.evaluate_board(game_state)}")
        print(f"Time2 Elapsed: {time.time() - start_time:.2f}s")

        print(f"Best move at depth {depth}: {best_move}, Score: {best_eval}")
        return best_eval, best_move
    

    def evaluate_board(self, game_state):
        e0 = {
            'wp': 1, 'wB': 3, 'wN': 3, 'wQ': 9, 'wK': 999,
            'bp': 1, 'bB': 3, 'bN': 3, 'bQ': 9, 'bK': 999
        }

        white_score = 0
        black_score = 0

        for row in game_state["board"]:
            for piece in row:
                if piece in e0:
                    if piece[0] == 'w':
                        white_score += e0[piece]
                    else:
                        black_score += e0[piece]

        board_eval = white_score - black_score
        return board_eval if self.ai_color == "white" else -board_eval


if __name__ == "__main__":
    game = MiniChess()
    game.play()