n = int(input())

for b in range(n):
    a = (n - 7 * b) / 4
    if (a.is_integer()):
        print("4" * int(a) + "7" * b)
        break
    if(7 * b > n):
        print(-1)
        break