def process(A, k):
    s = set([])
    for x in A:
        x = x % k
        if x not in s:
            s.add(x)
    s2 = set([])
    while len(s) > 0:
        for x in s:
            break
        for i in range(1, k+1):
            x2 = (i*x) % k
            if x2 not in s2:
                s2.add(x2)
        for x in s2:
            if x in s:
                s.remove(x)
    return sorted(list(s2))

n, k = [int(x) for x in input().split()]
A = [int(x) for x in input().split()]
answer = process(A, k)
print(len(answer))
print(' '.join(map(str, answer)))