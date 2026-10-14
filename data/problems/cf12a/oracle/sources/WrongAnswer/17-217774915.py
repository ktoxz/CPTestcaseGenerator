def is_symmetric_password(matrix):
   
    if matrix[1][1] != 'X':
        return "NO"  
    symmetric = (matrix[0][0] == matrix[2][2]) and \
                (matrix[0][1] == matrix[2][1]) and \
                (matrix[0][2] == matrix[2][0]) and \
                (matrix[1][0] == matrix[1][2])

    return "YES" if symmetric else "NO"


matrix = []
print("Enter the matrix (each row on a new line):")
for _ in range(3):
    row = list(input())
    matrix.append(row)


result = is_symmetric_password(matrix)
print(result)