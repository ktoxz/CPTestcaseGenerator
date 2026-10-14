def main():
    n, k = map(int, input().split())
    aa = {a % k for a in map(int, input().split())}
    if 1 in aa:
        print(k, ' '.join(map(str, range(k))), sep='\n')
        return
    aa.discard(0)
    rr = {0}
    for a in aa:
        rr |= {b for r in rr for b in range(r + a, k, a)}
    print(len(rr), ' '.join(map(str, sorted(rr))), sep='\n')


if __name__ == '__main__':
    main()