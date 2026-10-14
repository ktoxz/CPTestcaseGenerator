a = input()
m = 0
sums = sum(map(int, list(a)))

def funtus(x, m):
    x = list(str(x))
    print(x)
    s = sum(map(int, x))
    print(s)
    if s > 9:
        m += 1
        funtus(s, m)
        return m + 2
    else:
        return m + 1



if sums == 0:
   print(0)
elif sums > 0 and sums < 10:
    print(1)
else:
    print(funtus(a, 0))