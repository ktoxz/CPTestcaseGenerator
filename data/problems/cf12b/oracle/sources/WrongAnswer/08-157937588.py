import sys
input = sys.stdin.readline

n = list(map(int, list(input()[:-1])))
m = list(map(int, list(input()[:-1])))
x = sorted(n)
y = sorted(m)
if m[0] == 0 or x != y:
    print("WRONG_ANSWER")
else:
    if y[0] == 0:
        c = 0
        for i in range(len(y)):
            if y[i] != 0:
                c = i
                break
        y[c], y[0] = y[0], y[c]
    if y != m:
        print("WRONG_ANSWER")
    else:
        print("OK")