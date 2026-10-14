import math
k = int(input())
l = int(input())
if k != l:
    res1 = math.log(l) / math.log(k)
    res2 = math.log(l) / math.log(k)
    a = res1 == res2
    b = res1 and res2
    if int(b - 1) != 0:
        print("YES")
        print(int(b - 1))
    else:
        print("NO")
else:
    print("YES")
    print("1")