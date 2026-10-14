def nCr(n, r):
    s = 1
    for i in range(1, r+1):
        s = s * (n - r + i) / i
    return s
def sol():
    n, m, h = map(int, input().split())
    a = list(map(int, input().split()))
    n -= 1
    a[h - 1] -= 1
    total = sum(a)
    if total < n:
        print(-1)
        return
    totalM = total - a[h - 1]
    if totalM < n:
        print(1)
        return
    totalP = nCr(total, n)
    totalMP = nCr(totalM, n)
    ans = (totalP - totalMP) / totalP
    print(ans)

sol()