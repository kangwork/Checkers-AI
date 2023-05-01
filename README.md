# Checkers-Solver-AI
A friendly AI will create the best move possible to play against you! (Game Tree Search!)

## Description
This project is an implementation of an AI agent that solves endgame puzzles in the game of Checkers. The AI agent utilizes various algorithms, including minimax, alpha-beta pruning, and additional techniques, to find the best move possible given a specific puzzle configuration.

## Game Description
Checkers is a 2-player game played on an 8x8 chessboard.

- Players: One has black pieces, the other has red pieces.
- Objective: Capture all opponent's pieces.
- Game ends: when a player has no pieces or no legal moves.
- Initial setup: 12 red and 12 black pieces on dark squares of the first three rows on each side. Red player moves first, then turns alternate.

- Moves: 
  - Pieces move diagonally: one space if adjacent is empty, two spaces to capture opponent's piece.
  - Capturing involves jumping over opponent's piece onto an empty space.
  - Multiple captures can be made in a single move, including non-linear and multiple jumps.
  - If a player has a capturing opportunity, they must make a capture (force jump rule).
  - When a piece reaches opponent's end, it becomes a "king" and can move both forward and backward.

## Puzzle Configuration
The project focuses on solving endgame puzzles in Checkers. An endgame puzzle refers to a specific board configuration where a winning solution is guaranteed, provided the right set of moves is executed. These puzzles are challenging as they often require non-obvious moves or a large number of moves to reach a winning state.

The puzzle configurations are provided in text files, with each line representing a row from the Checkers board. The characters used in the text files represent different elements of the game:

- 'r' denotes a red piece
- 'b' denotes a black piece
- 'R' denotes a red king
- 'B' denotes a black king
- '.' (period character) denotes an empty square

For example, a puzzle layout may be represented as follows:

........<br />
....b...<br />
.......R<br />
..b.b...<br />
...b...r<br />
........<br />
...r....<br />
....B...<br />

In this case, the AI controls the red pieces, and it's the red player's turn to move.

## Input and Output Format
The program takes two command-line arguments: the input file and the output file. The input file contains the board configuration for the puzzle, represented as text. The output file will store the resulting board layout after the AI agent's move.

The board configuration is provided in the input file with each line representing a row of the Checkers board. The characters used in the configuration represent the elements of the game (red pieces, black pieces, red kings, black kings, and empty squares).

The AI agent's move, resulting in a new board layout, is saved in the output file using the same format as the input file. The output file should contain the best move possible given the input layout.

To run the program, use the following command:

`python3 checkers.py <input file> <output file>`

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
