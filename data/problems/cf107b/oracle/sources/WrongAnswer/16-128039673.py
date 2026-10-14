def f(n,h,s):
    a = s[h-1]
    b = sum(s)-a
    s = a+b
    if s==n: return 1
    if s<n:  return -1
    x = 1
    y = 1
    for i in range(n-1):
        x *= b-i
        y *= s-1-i
    return 1-x/y

n,m,h =      map(int,input().split())
s     = list(map(int,input().split()))
print(f(n,h,s))