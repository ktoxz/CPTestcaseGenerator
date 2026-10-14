#!/usr/bin/env python3

x3 = []
for i in range(3):
    row = input()
    x3.append(row)

def unique_pairs(n):
    for i in range(n):
        for j in range(i, n):
            yield i, j

def check_symmetry(array):
    result = True
    for i, j in unique_pairs(3):
        if array[i][j] == 'X' and array[2-i][2-j] != 'X':
            result = False
            break
    return result

if check_symmetry(x3):
    print('YES')
else:
    print('NO')