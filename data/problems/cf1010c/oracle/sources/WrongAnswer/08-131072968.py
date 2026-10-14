def gcd(a,b):
    if b == 0:
        return a
    return gcd(b,a%b)
n,k=map(int, input().split())
a=[int(v) for v in input().split()]
f=[0]*100010
g=0
for i in a:
    g=gcd(g,i)
print(k//g)
for i in range(k):
    if i%g==0:
        print(i, end=' ')