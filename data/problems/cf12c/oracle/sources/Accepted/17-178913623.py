import sys; R = sys.stdin.readline
n,m = map(int,R().split())
a = sorted(map(int,R().split()))
dic = {}
for _ in range(m):
    s = R()
    if s not in dic: dic[s] = 1
    else: dic[s] += 1
dic = sorted(dic.values(),reverse=True)
res1,res2 = 0,0
for i in range(len(dic)):
    res1 += a[i]*dic[i]
    res2 += a[-i-1]*dic[i]
print(res1,res2)