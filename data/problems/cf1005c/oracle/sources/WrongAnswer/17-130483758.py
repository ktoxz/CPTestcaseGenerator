import math

n = int(input())
l = list(map(int, input().split()))
unique = set(l)
doubled = list([x for x in l if l.count(x) >= 2])
cnt = len(unique)
for x in unique:
    for y in unique:
        # print(x, y, cnt)
        if x == y and x in doubled:
            if math.log2(x + y) == int(math.log2(x + y)):
                cnt -= 1
                break
        elif x != y:
            if math.log2(x + y) == int(math.log2(x + y)):
                cnt -= 1
                break
print(cnt)
# Fri Oct 01 2021 19:08:21 GMT+0300 (Москва, стандартное время)