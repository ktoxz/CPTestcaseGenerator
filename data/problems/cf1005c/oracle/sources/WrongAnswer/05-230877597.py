# Wadea #

import math
# print(math.log2(8))
# if float((math.log2(8))):
#     print("igbvifgbibv")
# if (2 ** math.log2(3)) == 3:
    
#     print(math.log2(8))
#     print(2**1.5)

n = int(input())
arr = list(map(int,input().split()))
if n == 1:
    print(1)
else:
    c = 0
    ans = 0
    l = 0
    while l < n:
        for j in range(n):
            if arr[j] != arr[l]:
                k = str(math.log2(arr[l] + arr[j]))
                k = k.split(".")
                if (2 ** math.log2(arr[l] + arr[j])) == arr[l] + arr[j] and k[1] == "0" and len(k[1]) == 1:pass
                else:c += 1
        if c == len(arr) - 1:
            ans += 1
        l += 1
        c = 0
    print(ans)