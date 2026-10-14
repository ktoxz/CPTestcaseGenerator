def main():
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    inf = 1e17
    mod = 10 ** 9 + 7

    # Max = 10 ** 1
    # primes = []
    # prime = [True for i in range(Max + 1)]
    # p = 2
    # while (p * p <= Max + 1):
    #
    #     # If prime[p] is not
    #     # changed, then it is a prime
    #     if (prime[p] == True):
    #
    #         # Update all multiples of p
    #         for i in range(p * p, Max + 1, p):
    #             prime[i] = False
    #     p += 1
    #
    # for p in range(2, Max + 1):
    #     if prime[p]:
    #         primes.append(p)
    #
    # print(primes)

    def factorial(n):
        f = 1

        for i in range(1, n + 1):
            f = (f * i) % mod  # Now f never can
        # exceed 10^9+7

        return f

    def ncr(n, r):
        # initialize numerator
        # and denominator
        num = den = 1
        for i in range(r):
            num = (num * (n - i)) % mod
            den = (den * (i + 1)) % mod
        return (num * pow(den,
                          mod - 2, mod)) % mod


    def solve(n):


        for i in range(math.ceil(n/7)+1):
            if (n - 7*i) % 4 == 0 and (n - 7*i)//4 >= 0:
                return '4'*((n - 7*i)//4)+'7'*i

        return '-1'


























        pass

    t = 1#int(input())
    ans = []
    for _ in range(t):
        n = int(input())
        #n,m = map(int, input().split())
        # s = input()
        # arr = [int(x) for x in input().split()]
        # a2 = [int(x) for x in input().split()]
        # grid = []
        # for i in range(n):
        #     grid.append(input())

        ans.append(solve(n))

    for answer in ans:
        print(answer)


if __name__ == "__main__":
    import sys, threading
    import bisect
    import math
    import itertools
    from sys import stdout

    # Sorted Containers
    import heapq
    from queue import PriorityQueue

    # Tree Problems
    sys.setrecursionlimit(2 ** 32 // 2 - 1)
    threading.stack_size(1 << 27)

    # fast io
    input = sys.stdin.readline

    thread = threading.Thread(target=main)
    thread.start()
    thread.join()