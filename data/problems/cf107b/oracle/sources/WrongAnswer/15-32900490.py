n, m, h = map ( int, input().split())
s = list ( map ( int, input().split()))
output = 0
if ( sum(s) < n ):
    output = -1
elif ( s [h-1] == 1 ):
    output = 0
else:
    n = n - 1
    a = sum(s) - 1
    output = n / a
print ( output )