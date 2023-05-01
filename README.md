# Checkers-AI
A friendly AI will create the best move possible to play against you! (Game Tree Search!)

Checkers Solver AI
This project is an implementation of an AI agent that solves endgame puzzles in the game of Checkers. The AI agent utilizes various algorithms, including minimax, alpha-beta pruning, and additional techniques, to find the best move possible given a specific puzzle configuration.

Game Description
Checkers is a classic 2-player board game played with distinct pieces. One player's pieces are black, and the other player's pieces are red. The game is typically played on an 8x8 chessboard, and the players take turns moving their pieces on the board.

Moving and capturing pieces are governed by the game's rules. The version of Checkers implemented in this project is the Standard English Draughts, which includes mandatory captures. The objective of the game is for each player to capture all of their opponent's pieces. The game ends when one player has no pieces remaining or has no legal moves left. If it's a player's turn but they can't move any of their pieces, that player loses the game.

The initial setup of the game involves placing 12 red pieces and 12 black pieces on the dark squares of the board across the first three rows on each side. The red player makes the first move, and the players take turns moving their pieces diagonally on the board.

Pieces can move in two ways:

Moving one space diagonally if the adjacent space is empty.
Moving two spaces diagonally if the adjacent space is occupied by the opponent, and the space beyond that is empty. In this case, the opponent's piece is captured.
If a move leads to a capture, and the moving piece ends up in a position where it can jump over another opponent's piece, the player has the option to continue moving and capture another piece. This sequence of moves can be non-linear and may involve multiple captures.

When a piece reaches the opponent's end of the board, it becomes a "king" and gains the ability to move both forward and backward.

Puzzle Configuration
The project focuses on solving endgame puzzles in Checkers. An endgame puzzle refers to a specific board configuration where a winning solution is guaranteed, provided the right set of moves is executed. These puzzles are challenging as they often require non-obvious moves or a large number of moves to reach a winning state.

The puzzle configurations are provided in text files, with each line representing a row from the Checkers board. The characters used in the text files represent different elements of the game:

'r' denotes a red piece
'b' denotes a black piece
'R' denotes a red king
'B' denotes a black king
'.' (period character) denotes an empty square

For example, a puzzle layout may be represented as follows:

........
....b...
.......R
..b.b...
...b...r
........
...r....
....B...

In this case, the AI controls the red pieces, and it's the red player's turn to move.

Input and Output Format
The program takes two command-line arguments: the input file and the output file. The input file contains the board configuration for the puzzle, represented as text. The output file will store the resulting board layout after the AI agent's move.

The board configuration is provided in the input file with each line representing a row of the Checkers board. The characters used in the configuration represent the elements of the game (red pieces, black pieces, red kings, black kings, and empty squares).

The AI agent's move, resulting in a new board layout, is saved in the output file using the same format as the input file. The output file should contain the best move possible given the input layout.

To run the program, use the following command:

python3 checkers.py <input file> <output file>

For example, python3 checkers.py input1.txt output1.txt will take the board layout stored in input1.txt, apply the AI agent's move, and save the resulting board layout in output1.txt.

## Achievements

- Utilizes the minimax algorithm to explore the game tree and determine the best move.

- Implements alpha-beta pruning to eliminate unnecessary branches of the game tree and improve efficiency.

- Sets a depth limit to control the search depth of the game tree.

- Incorporates a heuristic function to estimate the value of non-terminal states when the depth limit is reached.

- Considers factors such as the number of pieces, position of pieces, and strategic considerations in the heuristic function.

- Implements state caching to store previously evaluated board states and their utility values.

- Retrieves utility values from the cache for already evaluated board states to avoid redundant computations.

- Reduces computational overhead and improves performance by avoiding recomputation of utility values.

- Balances between exploring the game tree and making informed decisions within the time limit.

- Provides a challenging gameplay experience for the players by making optimal moves based on the evaluation criteria.

- Adheres to the input/output requirements and passes the provided validation script.

- Manages memory efficiently to avoid running out of memory during program execution.

- Optimizes the program to handle the exponential growth of moves with the depth of the game tree.

- Implements pruning techniques and efficient algorithms to explore the search space effectively.

- Demonstrates correctness and performance within the specified time and space constraints.

## Note
This project was for a course CSC384H1: Introduction to Artificial Intelligence.
