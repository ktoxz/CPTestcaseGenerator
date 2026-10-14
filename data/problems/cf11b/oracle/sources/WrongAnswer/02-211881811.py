import math

def next_triangle(n):
    return math.ceil((-1 + math.sqrt(8 * n + 1)) / 2) * (math.ceil((-1 + math.sqrt(8 * n + 1)) / 2) + 1) // 2

def next_triangle_index(n):
    return math.floor(math.sqrt(8 * next_triangle(n) + 1) - 1) // 2

def steps(n):
    if n == 0:
        return 0
    return next_triangle_index(n) + steps(next_triangle(n)-n)

x = abs(int(input()))

print(steps(x))