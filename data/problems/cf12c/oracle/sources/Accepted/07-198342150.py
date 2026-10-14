from collections import Counter
n,m=map(int,input().split())
s=list(map(int,input().split()))
d=dict(Counter([input() for _ in range(m)]))
mi=0
ma=0
s1=s.copy()
s2=s.copy()
skd=list(d.values())
skd=sorted(skd,reverse=True)
#print(skd)
for i in skd:
     for j in range(len(s1)):
          if s1[j]==min(s1):
               mi+=s1[j]*i
               s1.pop(j)
               break
for i in skd:
     for j in range(len(s2)):
          if s2[j]==max(s2):
               ma+=s2[j]*i
               s2.pop(j)
               break
print(mi,ma)