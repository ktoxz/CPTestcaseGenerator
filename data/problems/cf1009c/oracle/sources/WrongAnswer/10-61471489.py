import sys

lines = []
for Line in sys.stdin:
  lines.append(Line.rstrip('\n'))

# lines=["2 3",
# "-1 3",
# "0 0",
# "-1 -4"]

# lines=["3 2",
# "0 2", 
# "5 0"]


n,m = list(map(int,lines[0].split()))
del(lines[0])

x=[]
d=[]
for i in range(m):
  a,b = list(map(int,lines[i].split()))
  x+=[a]
  d+=[b]

v=[0 for i in range(n)]

p=n-1
for j in range(m):
    for i in range(n):
        v[i]+= x[j]+d[j]*(p-i)
print(sum(v)/len(v))