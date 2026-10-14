x = input().split()
n = int(x[0])
m = int(x[1])
y = input().split()
for i in range(0,n):
    y[i] = int(y[i])
y.sort()
y2 = y[::-1]
D = {}
for i in range(0,m):
    x = input()
    if x in D:
        D[x] += 1
    else:
        D[x] = 1
T = list(D.values())
T = list(reversed(T))
best = 0
for i in T:
    best += y[0]*i
    y.remove(y[0])

worst = 0
for i in T:
    worst += y2[0]*i
    y2.remove(y2[0])

print(best,worst)