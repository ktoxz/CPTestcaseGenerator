def gcd(a, b):
    while a != b:
        if a > b:  a -= b
        else: b -= a
    return a


a, b, n = map(int, input().split())
gcd_val = gcd(a, n)
winner = 0
while gcd_val < n:
    gcd_val = gcd(a, n)
    n -= gcd_val
    winner = 1 if winner == 0 else 0

print(winner)