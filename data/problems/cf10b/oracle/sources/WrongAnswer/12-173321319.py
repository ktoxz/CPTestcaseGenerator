import math

n, k = [int(i) for i in input().split()]
people = [int(i) for i in input().split()]
room = []
for i in range(k):
    b = []
    for i in range(k):
        b.append(0)
    room.append(b)
for i in range(n):
    ans = 100000000000000000
    ansind = [0, 0, 0]
    xc = math.ceil(k / 2)
    yc = math.ceil(k / 2)
    for riad in range(k):
        for mesto in range(n):
            prov = False
            ansnow = 0
            for j in range(mesto, mesto + people[i]):
                if j < k and room[riad][j] != 1:
                    ansnow += abs(xc - riad - 1)
                    ansnow += abs(yc - mesto - 1)
                else:
                    prov = True
                    break
            if prov is False:
                if ansnow < ans:
                    ans = ansnow
                    ansind = [riad + 1, mesto + 1, mesto + people[i]]
    if ansind != [0, 0, 0]:
        print(*ansind)
        for j in range(ansind[1] - 1, ansind[2]):
            room[ansind[0] - 1][j] = 1
    else:
        print(-1)