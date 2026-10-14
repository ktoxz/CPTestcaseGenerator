n, m = map(int, input().split())
M = m
while m:
    n1, n2 = map(int, input().split())
    m = m - 1
if M == n:
    print("FHTAGN!")
else:
    print('NO')