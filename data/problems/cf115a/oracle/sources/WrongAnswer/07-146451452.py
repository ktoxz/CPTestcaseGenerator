a=int(input())
d={}
for i in range(0,a):
    b=int(input())
    if b not in d:
        d[b]=1
print(len(d))