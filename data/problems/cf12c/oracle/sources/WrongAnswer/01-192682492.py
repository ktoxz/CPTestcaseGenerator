a,b=map(int,input().split())
d=[]
c=[int(i) for i in input().split()]
for i in range(b):
    e=input()
    if d.count(e)==0:
        d=d+[e]
c.sort()
k=b-len(d)
print(sum(c[0:len(d)])+k*c[0],sum(c[-len(d):-1])+(k+1)*c[-1])