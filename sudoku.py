import sys

def read_file(textfile):
    f=open(textfile, 'r')
    next(f)
    i = 0
    j = 0
    matrix = [[0 for x in range(9)] for y in range(9)]
    # print(matrix)
    
    while True:
        j = 0
        char = f.readline()
        for c in char:
            matrix[i][j] = int(c)
            # print(i,j)
            j+=1
            if j == 9:
                i+=1
                break
        if i == 9:
            break
    return matrix

def read_file(textfile):
    """Read a 9x9 Sudoku grid from a text file into a matrix of ints."""
    matrix = []
    with open(textfile, 'r') as f:
        next(f)  # skip header line
        for _ in range(9):  # read 9 lines
            line = f.readline().strip()  # strip newline/spaces
            row = [int(c) for c in line[:9]]  # only first 9 chars
            matrix.append(row)
    return matrix

def check_sudoku(row, column, number, matrix_board) -> bool:
    check = 0
    for i in range(0,9):
        if matrix_board[row][i]==number:
            check=1
    for i in range(0,9):
        if matrix_board[i][column]==number:
            check=1
            
    row=row-row%3
    column=column-column%3
    
    for i in range(0,3):
        for j in range(0,3):
            if matrix_board[row+i][column+j]==number:
                check=1
                
    return False if check==1 else True

class Calls:
    number_of_calls=0
c = Calls()

def sudoku_solver(matrix):
    c.number_of_calls=c.number_of_calls+1
    break_condition=0
    for i in range(0,9):
        for j in range(0,9):
            if matrix[i][j]==0:
                break_condition=1
                row=i
                column=j
                break
    
    if break_condition==0:
        print("Naive Backtracking Algorithm Solution: ")
        for i in matrix:
            print(i)
        print("Amount of Recursions")
        print(c.number_of_calls)
        exit(0)
        
        for i in range(0,10):
            if check_sudoku(row, column, i, matrix):
                matrix[row][column]=i
                if sudoku_solver(matrix):
                    return True
                matrix[row][column]=0
        return False
    
matrix=read_file(sys.argv[1])
sudoku_solver(matrix)