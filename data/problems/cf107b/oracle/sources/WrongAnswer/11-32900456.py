n, m, h = map ( int, input().split())
s = list ( map ( int, input().split()))
output = 0
if ( sum(s) < n or s[h-1] == 1 ):
    output = -1
else:
    n = n - 1
    a = sum(s) - 1
    output = n / a
print ( output )