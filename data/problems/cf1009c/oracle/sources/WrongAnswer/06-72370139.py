n,m = map(int ,input().split())
otv1 = 0.0
otv2 = 0.0
otv3 = 0.0
otv4 = 0.0
m1 = n // 2
m2 = n // 2
if n % 2 == 0:
    m1 -= 1
for i in range(m):
    a,b = map(int, input().split())
    otv1 += a
    if b > 0:
        otv2 += b
    else:
        otv3 += b
        otv4 += b
otv2 *= (n * (n - 1) / 2)
otv3 *= m1 * (m1 + 1) / 2
otv4 *= m2 * (m2 + 1) / 2
print("%.10f" % (otv1 + (otv2 + otv3 + otv4) / n))