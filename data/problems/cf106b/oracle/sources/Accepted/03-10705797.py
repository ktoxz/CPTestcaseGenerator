n, l = int(input()), []
for i in range(n):
    s, r, h, c = map(int, input().split())
    l.append((c, s, r, h, i + 1))
l.sort()
for li in l:
    if all(li[1] >= lj[1] or li[2] >= lj[2] or li[3] >= lj[3] for lj in l):
        print(li[4])
        exit()