# Sudokrypt

A robust, object-oriented backtracking Sudoku solver written in Python.
It reads a 9×9 Sudoku puzzle from a text file, validates the input, and prints the solution (if any) along with diagnostic information such as recursion count and optional timing.

---

## Features

* Reads Sudoku puzzles from text files (9 rows of 9 digits or `.`/`0` for blanks).
* Optionally skips the first line of the file (for header or metadata).
* Robust input validation with clear error messages.
* Object-oriented design (`SudokuSolver` class) with reusable methods.
* Naive backtracking algorithm with recursion count tracking.
* Optional timing output.

---

## Installation

You need **Python 3.8+** (no external dependencies required beyond the standard library).

Clone this repository:

```bash
git clone https://github.com/MicheleGrieco/Sudokrypt.git
cd sudokrypt
```

---

## Usage

### 1. Prepare your puzzle file

The solver expects a text file containing a Sudoku puzzle in one of these formats:

**Compact digits:**

```
530070000
600195000
098000060
800060003
400803001
700020006
060000280
000419005
000080079
```

**Space-separated tokens:**

```
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

Use `.` instead of `0` if you prefer.

If your file has a header line before the puzzle, run the solver with `--skip-header`.

---

### 2. Run the solver from the command line

Basic command:

```bash
python sudoku_solver.py puzzle.txt
```

Optional flags:

* `--skip-header`: skip the first line of the file.
* `--time`: measure and display elapsed solving time.

**Examples:**

```bash
# Solve a puzzle
python sudoku_solver.py puzzles/easy.txt

# Solve a puzzle and show execution time
python sudoku_solver.py puzzles/easy.txt --time

# Skip a header line and show execution time
python sudoku_solver.py puzzles/with_header.txt --skip-header --time
```

**Example Output:**

```
Initial board:
5 3 . . 7 . . . .
6 . . 1 9 5 . . .
. 9 8 . . . . 6 .
...

Solved: True (time: 0.002345s, recursive calls: 312)

Solution:
5 3 4 6 7 8 9 1 2
6 7 2 1 9 5 3 4 8
1 9 8 3 4 2 5 6 7
...
```

---

### 3. Reusing the solver programmatically

```python
from sudoku_solver import SudokuSolver

solver = SudokuSolver.from_file("puzzle.txt")
if solver.solve():
    solver.pretty_print()
else:
    print("Puzzle is unsolvable.")
```

---

## Docker Support

You can build and run the solver inside a Docker container for portability.

### Build the Docker image

```bash
docker build -t sudoku-solver .
```

### Run the solver inside Docker

Mount your puzzle file into the container and run:

```bash
docker run --rm -v "$PWD":/app sudoku-solver puzzle.txt --time
```

This mounts the current directory into `/app` inside the container so the solver can access your `puzzle.txt`.

---
