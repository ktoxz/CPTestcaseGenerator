import math
k = int(input())
a = int(input())
res1 = math.log(a) / math.log(k)
res2 = math.log(a) / math.log(k)
b = res1 and res2
if a == k:
    print("YES")
    print("0")
elif a/k == int(a/k):
    if k == 10 and a >= 1000:
        c = k ** int(b + 1)
    else:
        c = k ** int(b)
    if c == a:
        print("YES")
        print(int(b))
    else:
        print("NO")
else:
    print("NO")