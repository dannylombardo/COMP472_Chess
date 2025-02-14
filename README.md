# COMP472_Chess

## Project Description
MiniChess is a simplified form of chess that is played on a 5x5 board. With fewer pieces and a smaller board, the game is played according to standard chess rules. The objective is to checkmate the opponent's king or force a draw. Automatic game logging, piece-specific movement logic, and move validation are all implemented in the game.

## How to Run the Project

### Prerequisites
- Python 3.X installed

### Running the Game
1. Clone the repository or download the source code.
2. Open a terminal or command prompt in the project directory.
3. Run the following command:
   ```sh
   python MiniChessSkeletonCode.py
   ```

## Features
- **Board Initialization**: The game starts with a predefined 5x5 board layout.
- **Move Validation**: Ensures only legal moves are played.
- **Piece Movements**: Implements movement logic for King, Queen, Bishop, Knight, and Pawn.
- **Game Turns**: Alternates turns between white and black players.
- **Checkmate & Draw Detection**: The game ends when a king is eliminated or when 10+ moves occur without a capture.
- **Game Logging**: Moves are recorded in `COMP472_Project.txt`.

## New Classes and Functions
- **MiniChess**: Main class handling game state, move validation, and board updates.
- **valid_moves(self, game_state)**: Generates all legal moves for the current player.
- **get_piece_moves(self, board, row, col, piece)**: Determines valid moves for a given piece type.
- **make_move(self, game_state, move)**: Executes a move and checks for game-ending conditions.
- **display_board(self, game_state)**: Prints the current state of the board.

## Notes
- The game will print the board after each move and indicate when a player wins.
- The log file `COMP472_Project.txt` keeps track of all moves and game results.
