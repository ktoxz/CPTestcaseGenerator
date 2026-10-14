def main():
    n, k = map(int, input().split())
    aa = set(a % k for a in map(int, input().split()))
    if 1 in aa:
        r = list(range(k))
    else:
        aa.discard(0)
        r = [False] * k
        r[0] = True
        k -= 1
        for a in aa:
            r[a::a] = (True,) * (k // a)
        r = [i for i, f in enumerate(r) if f]
    print(len(r))
    print(' '.join(map(str, r)))


if __name__ == '__main__':
    main()