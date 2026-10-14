n=int(input())
a=list(map(int,input().split()))
z=(sum(a)+len(a)-1)
del a[-1]
s=a.count(1)
print(z-s)