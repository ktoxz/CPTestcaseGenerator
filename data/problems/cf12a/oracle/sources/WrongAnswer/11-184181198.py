l = [i for i in input()]
l += [i for i in input()]
l += [i for i in input()]

for i in range(9):
    l[i] = i+1 if l[i] == 'X' else 0

s = sum(l)
if s > 0 and (s % 5 == 0 or s % 10 == 0):
    print('YES')
else:
    print('NO')