from collections import defaultdict
dc = defaultdict(int)
n,m,k = input().split()
n = int(n)
m = int(m)
k = float(k)
l = []
for i in range(n):
    st,st1 = input().split()
    if(int(int(st1)*k)>=100):
        dc[st] = int(int(st1)*k)
        l.append([st,int(int(st1)*k)])
for i in range(m):
    s = input()
    if(dc[s]==0):
        l.append([s,0])
l.sort()
for i in l:
    print(i[0],i[1])