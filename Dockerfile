# Use the official Python image as base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the solver script into the container
COPY sudoku_solver.py /app/sudoku_solver.py

# Default command: show help
ENTRYPOINT ["python", "sudoku_solver.py"]
CMD ["-h"]