s = list(input())
k = int(input())
n = len(s)
if k >= n:
    print(0)
    print()
else:
    lst = sorted(s, key=s.count, reverse=True)[:n-k]
    print(len(lst))
    print("".join(lst))