I=lambda:map(int,input().split())
n,a,b,c,u,v=I()
exec('x=['+n*'[*I()],'+']')
r=0
for i in range(n):
  r+=a*(x[i][1]-x[i][0])
  if i:
    t=x[i][0]-x[i-1][1]
    s=min(t,u);r+=s*a;t-=s
    s=min(t,v);r+=s*b;t-=s
    r+=t*c
print(r)