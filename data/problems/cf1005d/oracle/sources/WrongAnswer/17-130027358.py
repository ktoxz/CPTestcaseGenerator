st = input()

n = len(st)

res = 0
pred_start = 0

for i in range(n):
    if (int(st[i]) % 3 == 0):
        res += 1
        pred_start = i + 1
    elif (sum (int(j) for j in st[pred_start:i + 1]) % 3 == 0):
        pred_start =i + 1
        res += 1
    
print(res)