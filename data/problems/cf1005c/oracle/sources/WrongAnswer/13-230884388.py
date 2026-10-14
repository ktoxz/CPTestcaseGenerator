# Wadea #

import math
n = int(input())
arr = list(map(int,input().split()))
if n == 1:
    print(1)
else:
    c = 0
    ans = 0
    l = 0
    arr1 = []
    passs = set()
    while l+1 < n:
        for j in range(l+1,n):
                k = str(math.log2(arr[l] + arr[j]))
                k = k.split(".")
                if (2 ** math.log2(arr[l] + arr[j])) == arr[l] + arr[j] and k[1] == "0" and len(k[1]) == 1:
                    passs.add(arr[j])
                    passs.add(arr[l])
        l += 1
    print(len(set(arr)) - len(passs))