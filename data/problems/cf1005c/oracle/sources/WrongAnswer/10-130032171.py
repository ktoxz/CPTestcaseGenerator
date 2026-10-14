from collections import Counter
n = int(input())
nums = list(map(int, input().split()))
nums_1 = Counter(nums)
k = 0
while (1 << k) < 10 ** 9:
    k += 1
ans = 0
for x in nums:
    fl = True
    for j in range(k):
        dist = (1 << j) - x
        if (nums_1[dist] > 1 or (dist != x and nums_1[dist] == 1)) and nums_1[dist] != 0:
            fl = False
    if fl:
        ans += 1
print(ans)


# Mon Sep 27 2021 21:24:05 GMT+0300 (Москва, стандартное время)