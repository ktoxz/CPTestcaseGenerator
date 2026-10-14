n = int(input())
a = list(input())
b = list(input())
posA = []
posB = []
for i in range(n//2):
    posA.append([a[i],a[n-i-1]])
    posB.append([b[i],b[n-i-1]])
if n % 2 != 0:
    posA.append([a[n//2]])
    posB.append([b[n//2]])
ans = 0
for i in range(len(posA)):
    if len(posA[i]) == len(posB[i]) and len(posA[i]) == 1:
        if posA[i][0] != posB[i][0]:
            ans += 1
    if len(set(posA[i])) != len(set(posB[i])):
        if len(set(posA[i])) > len(set(posB[i])):
            if posB[i][0] in posA[i]:
                 ans += 1
            else:
                ans += 2
        else:
            if posA[i][0] in posB[i]:
                 ans += 1
            else:
                ans += 2
print(ans)