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

