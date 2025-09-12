#!/usr/bin/env python3
"""
Module name: sudoku_solver.py
Author: Michele Grieco
Description:
    A safe, readable, object-oriented backtracking Sudoku solver.
Usage:
    python sudoku_solver.py puzzle.txt         # reads puzzle.txt and solves it
    python sudoku_solver.py -h                 # for help

Input file format:
- By default, expects exactly 9 lines of puzzle data, each containing 9 characters
  (digits 1-9 or 0/. for empty) or 9 whitespace-separated tokens.
- If the file has a 1-line header, run with --skip-header to ignore the first line.
"""

from __future__ import annotations
import argparse                    # for robust command-line parsing
import sys                         # for exit codes and argv fallback
from typing import List, Optional  # type hints
from time import perf_counter      # optional timing for performance info


class SudokuSolver:
    """Class encapsulating a 9x9 Sudoku board and a backtracking solver."""

    def __init__(self, board: Optional[List[List[int]]] = None) -> None:
        """
        Initialize the SudokuSolver with an optional board. If no board is provided,
        initializes an empty 9x9 board.
        Args:
            board: Optional 9x9 list of lists of integers (0-9), where 0 represents empty cells.
        """
        self.board: List[List[int]] = board if board is not None else [[0] * 9 for _ in range(9)]
        self.recursive_calls: int = 0 # Counter for how many recursive calls were performed (for diagnostics).

    @staticmethod
    def parse_line_to_row(line: str) -> List[int]:
        """
        Convert a single line of text into a row of 9 integers.
        Accepts either a compact string of 9 characters (e.g. "530070000")
        or space-separated tokens (e.g. "5 3 0 0 7 0 0 0 0").
        Uses 0 for blanks ('.' or '0').
        Args:
            line: A string representing one row of the Sudoku puzzle.
        Returns:
            A list of 9 integers (0-9) representing the row.
        """
        # Strip line ending and surrounding whitespace.
        raw = line.strip()

        # If empty after stripping, it's invalid for a row.
        if not raw:
            raise ValueError("Empty line encountered where a Sudoku row was expected.")

        # If the line contains whitespace, split into tokens.
        if any(ch.isspace() for ch in raw):
            tokens = raw.split()  # split on whitespace
            if len(tokens) != 9:
                raise ValueError(f"Expected 9 tokens in row but got {len(tokens)}: {raw!r}")
            row: List[int] = []
            for token in tokens:
                if token == '.' or token == '0':
                    row.append(0)
                else:
                    # Validate each token is a single digit between 1 and 9.
                    if len(token) != 1 or not token.isdigit() or not (1 <= int(token) <= 9):
                        raise ValueError(f"Invalid token in Sudoku row: {token!r}")
                    row.append(int(token))
            return row

        # Otherwise treat as a compact string of characters.
        if len(raw) != 9:
            raise ValueError(f"Expected 9 characters in row but got {len(raw)}: {raw!r}")

        row = []
        for ch in raw:
            if ch == '.' or ch == '0':
                row.append(0)
            else:
                if not ch.isdigit() or not (1 <= int(ch) <= 9):
                    raise ValueError(f"Invalid character in Sudoku row: {ch!r}")
                row.append(int(ch))
        return row

    @classmethod
    def from_file(cls, path: str, skip_header: bool = False) -> SudokuSolver:
        """
        Read a Sudoku puzzle from a file and return a SudokuSolver instance.
        Will raise informative exceptions on malformed input.
        Args:
            cls: The class to instantiate (SudokuSolver).
            path: Path to the input file.
            skip_header: If True, skip the first line of the file (header).
        Returns:
            An instance of SudokuSolver with the board initialized from the file.
        Raises:
            IOError, OSError: If the file cannot be read.
            ValueError: If the file format is invalid (wrong number of rows/columns, invalid characters).
        """
        # Read file using a context manager so the file is always closed.
        with open(path, "r", encoding="utf-8") as fh:
            # Optionally skip a header line if the user requests that.
            if skip_header:
                _ = fh.readline()

            rows: List[List[int]] = []
            # Read up to 9 non-empty lines (we allow blank lines to be skipped).
            while len(rows) < 9:
                line = fh.readline()
                if line == "":  # EOF reached
                    break
                # Ignore fully blank lines (but don't skip meaningful whitespace lines).
                if line.strip() == "":
                    continue
                # Parse the line into a row of 9 ints (raises on error).
                rows.append(cls.parse_line_to_row(line))

            if len(rows) != 9:
                raise ValueError(f"Expected 9 puzzle rows in file {path!r}, but found {len(rows)}.")

        # Validate final shape and return instance.
        for r in rows:
            if len(r) != 9:
                raise ValueError("Internal error: parsed row does not have length 9.")
        return cls(board=rows)

    def is_valid_placement(self, row: int, col: int, num: int) -> bool:
        """
        Check whether placing `num` at (row, col) is legal according to Sudoku rules.
        Args:
            row: Row index (0-8).
            col: Column index (0-8).
            num: Number to place (1-9).
        Returns:
            True if placing num at (row, col) is valid, False otherwise.
        """
        # Check row for conflicts.
        for c in range(9):
            if self.board[row][c] == num:
                return False

        # Check column for conflicts.
        for r in range(9):
            if self.board[r][col] == num:
                return False

        # Check 3x3 subgrid for conflicts.
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False

        # No conflicts found, placement is valid.
        return True

    def find_empty_cell(self) -> Optional[tuple[int, int]]:
        """
        Find an empty cell on the board (value 0).
        Returns a tuple (row, col) or None if the board is full.
        Returns:
            A tuple (row, col) of the first empty cell found, or None if no empty cells exist.
        """
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def solve(self) -> bool:
        """
        Solve the Sudoku board using naive backtracking.
        The solver mutates self.board in-place.
        Returns:
            True if the puzzle was solved, False if no solution exists.
        """
        # Increment recursion counter for diagnostics.
        self.recursive_calls += 1

        # Find an empty cell; if none, puzzle is solved.
        found = self.find_empty_cell()
        if found is None:
            return True  # solved

        row, col = found

        # Try digits 1 through 9 in the empty cell.
        for num in range(1, 10):
            if self.is_valid_placement(row, col, num):
                # Place the candidate and recurse.
                self.board[row][col] = num
                if self.solve():
                    return True  # propagate success upward
                # Backtrack if placing num did not lead to a solution.
                self.board[row][col] = 0

        # No candidate worked here; signal failure to caller to backtrack.
        return False

    def pretty_print(self) -> None:
        """Print the board in a human-readable format."""
        for r in range(9):
            row = self.board[r]
            # join digits but show '.' for blanks
            printable = " ".join(str(x) if x != 0 else "." for x in row)
            print(printable)


def main(argv: Optional[List[str]] = None) -> int:
    """
    Command-line entry point.
    Args:
        argv: Optional list of command-line arguments (defaults to sys.argv[1:] if None).
    Returns:
        Exit code: 0 on success, non-zero on failure.
    """
    # Use provided argv or default to sys.argv[1:].
    argv = argv if argv is not None else sys.argv[1:]

    # Set up a minimal and robust argument parser.
    parser = argparse.ArgumentParser(description="Solve a 9x9 Sudoku puzzle from a text file.")
    parser.add_argument("file", help="Path to input file containing the puzzle.")
    parser.add_argument("--skip-header", action="store_true", help="Skip the first line of the file (header).")
    parser.add_argument("--time", action="store_true", help="Print elapsed time for solving.")
    args = parser.parse_args(argv)

    try:
        # Create solver instance from the input file (validates format).
        solver = SudokuSolver.from_file(args.file, skip_header=args.skip_header)
    except (IOError, OSError) as e:
        # File I/O errors (file not found, permission denied, etc.)
        print(f"Error reading file {args.file!r}: {e}", file=sys.stderr)
        return 2
    except ValueError as ve:
        # Parsing/validation errors (malformed file)
        print(f"Input error: {ve}", file=sys.stderr)
        return 3

    # Optionally report initial board for debugging.
    print("Initial board:")
    solver.pretty_print()
    print()

    # Time the solving if requested.
    start = perf_counter() if args.time else None

    # Attempt to solve; returns True if solved.
    solved = solver.solve()

    # Stop timing and report.
    if args.time and start is not None:
        elapsed = perf_counter() - start
        print(f"\nSolved: {solved} (time: {elapsed:.6f}s, recursive calls: {solver.recursive_calls})")
    else:
        print(f"\nSolved: {solved} (recursive calls: {solver.recursive_calls})")

    # Print final board if solved.
    if solved:
        print("\nSolution:")
        solver.pretty_print()
        return 0
    else:
        print("\nNo solution found. The puzzle may be invalid or unsolvable.", file=sys.stderr)
        return 4


if __name__ == "__main__":
    # Run main with system argv and exit with returned code.
    raise SystemExit(main())
