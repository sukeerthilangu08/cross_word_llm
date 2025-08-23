# Command-Line Crossword Generator

This project is a command-line tool for automatically generating crossword puzzles. It takes a list of words and a desired grid size to construct a valid crossword grid.

## Features

*   **Dynamic Grid Size:** The user can specify the desired grid size.
*   **Symmetric Black Square Placement:** Black squares are added to the grid with 180-degree rotational symmetry.
*   **Intelligent Word Placement:** The script uses a backtracking algorithm to find a valid placement for the words, prioritizing intersections.
*   **User-Friendly:** Prompts the user for confirmation and grid size.

## Requirements

*   Python 3.x

## How to Use

1.  Make sure you have a file named `words.txt` in the same directory as the script, containing a list of words (one word per line).
2.  Run the script from your terminal:
    ```bash
    python crossword_generator.py
    ```
3.  The script will ask for confirmation to start the generation. Enter `yes`.
4.  You will then be prompted to enter the desired grid size (e.g., `15` for a 15x15 grid).
5.  The script will then display the initial grid with black squares and, if successful, the final grid with the placed words.

## Input Files

*   `words.txt`: A plain text file containing a list of words to be used in the crossword, with one word per line.

## Output

The script will output two grids to the command line:
1.  The initial empty grid with symmetrically placed black squares (`#`).
2.  The final generated crossword grid with the words filled in.

If a valid crossword cannot be generated with the given words and grid size, a message will be displayed.

## Algorithm

The generator uses a backtracking algorithm to place words. It sorts words by length in descending order and attempts to place them one by one. For a word to be placed, it must fit on the grid without overwriting existing letters (unless it's a valid intersection) and must not be adjacent to other words unless it's part of an intersection. If the script gets stuck, it backtracks and tries a different placement.
