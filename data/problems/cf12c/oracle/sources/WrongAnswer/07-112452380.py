k=0
r=0
n, m = map(int, input().split())
pt = sorted(map(int, input().split()))[:n]
for i in range(0,m):
    k+=pt[i]
for i in range(m,0,-1):
    r+=pt[i]
print(k,r)