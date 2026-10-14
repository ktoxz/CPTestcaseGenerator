c=[]
y=0
x=0
final=[]
a=int (input())
for i in range (a):
  b=int(input())
  c.append(b)
for i in range(1,len(c)+1):
  for e in c:
    if e==i:
      x=x+1
  final.append(x)
  x=0
for i in final:
  if i!=0:
    y=y+1
print(y+1)