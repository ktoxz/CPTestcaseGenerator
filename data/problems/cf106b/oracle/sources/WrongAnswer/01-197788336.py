def mide(s):
     r=0
     for y in s.split():
          r+=int(y)
     r/=len(s.split())
     return r
s=int(input())
m=[mide(input()) for _ in range(s)]
for i in range(s):
     if m[i]==max(m):
          print(i+1)
          break
print(m)