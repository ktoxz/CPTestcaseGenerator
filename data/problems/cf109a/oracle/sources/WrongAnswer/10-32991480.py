from itertools import permutations

def main(n):
    m = int(2e9)
    for x in range(1, 99):
        y = (n - 4 * x) / 7
        if y < 0:
            break
        if 4 * x + int(7 * y) == n and x >= 0 and y >= 0:
            l = []
            for i in range(x):
                l.append(4)
            for j in range(int(y)):
                l.append(7)
            p = int(''.join(list(map(str,l))))
            m = min(p, m)
    if m == int(2e9):
        return -1
    return m

print(main(int(input())))