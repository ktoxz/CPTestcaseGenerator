n, d = map(int, input().split())
b = list(map(int, input().split()[:n]))

b_addlowest = min(b) + d
b.insert(0, b_addlowest)    
b.remove(min(b))
k = len(b)
moves = 0

for i in range(k):
    already_sorted = True
    for j in range(k - i - 1):
        if b[j] > b[j + 1]:
            b[j], b[j + 1] = b[j + 1], b[j]
            moves += 1
            already_sorted = False
    if already_sorted:
            break
print(moves)