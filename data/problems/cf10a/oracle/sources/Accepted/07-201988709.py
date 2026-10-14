def find_length(n):
    r = 0
    while n != 0:
        n = n // 10
        r += 1
    return r


def count_zeros(n):
    r = 0
    while n != 0:
        if n % 10 == 0:
            r += 1
        else:
            break
        n = n // 10
    return r


def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a, b):
    return a * b / gcd(a, b)


def remove_all_zero(n):
    while (n != 0) & (n % 10 == 0):
        n = n / 10
    return n


def is_prime(n):
    if n == 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def sieve(n):
    arr = [True] * (n + 1)
    i = 2
    while i * i <= n:
        if is_prime(i):
            j = i * i
            while j <= n:
                arr[j] = False
                j += i
        i += 1
    return [i for i in range(2, n + 1) if arr[i]]


def get_all_subsequences(s):
    n = len(s)
    r = []
    for i in range(1, 1 << n):
        x = ''
        for j in range(n):
            if (i >> j) & 1:
                x += s[j]
        r.append(x)
    return r


def if_sorted(arr):
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False
    return True


##################################################################

# find_length(n)
# count_zeros(n)
# factorial(n)
# gcd(a, b)
# lcm(a, b)
# remove_all_zero(n)
# is_prime(n)
# sieve(n)
# get_all_subsequences(s)


##################################################################

class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None


def main():
    # n, k = tuple(map(int, input().strip().split()))
    # n = list(map(int, input().strip().split()))[0]
    a = list(map(int, input().strip().split()))
    arr = []
    for i in range(a[0]):
        r = 0
        m, n = tuple(map(int, input().strip().split()))
        arr.append((m, n))
    r, p = 0, 0
    for m, n in arr:
        r += (n - m) * a[1]
        if p == 0:
            p = n
            continue
        x = m - p
        if x >= (a[4] + a[5]):
            r += (x - (a[4] + a[5])) * a[3]
            r += a[5] * a[2]
            r += a[4] * a[1]
        elif x >= a[4]:
            r += (x - a[4]) * a[2]
            r += a[4] * a[1]
        else:
            r += x * a[1]
        p = n
    print(r)


if __name__ == '__main__':
    main()