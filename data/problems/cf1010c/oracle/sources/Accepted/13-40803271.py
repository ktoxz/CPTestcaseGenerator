import sys
import os

def gcd(a, b):
    if a > b:
        return gcd(b, a)
    if a == 0:
        return b
    return gcd(b % a, a)

def build(n, d):
    print(n // d)

    r = []
    for i in range(n // d):
        r.append(i * d)

    print(' '.join(map(str, r)))

def solve(k, a):
    d = k
    for note in a:
        d = gcd(note, d)
        if d == 1:
            return build(k, d)

    return build(k, d)

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    solve(k, a)

if __name__ == '__main__':
    main()