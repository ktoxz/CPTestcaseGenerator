import sys
input = sys.stdin.readline


def solve(s):
    num, s = s, str(s)
    isDivisible = {}
    n = len(s)
    for i in range(n):
        curr = int(s[i])
        if curr % 3 == 0:
            isDivisible[(i, i)] = True
        if curr == 0:
            continue
        for j in range(i+1, n):
            curr += int(s[j])
            isDivisible[(i, j)] = False if curr % 3 != 0 else True

    dp = [0]*n
    for i in range(n):
        dp[i] = 1 if (0, i) in isDivisible else 0
        for j in range(i):
            if (j+1, i) in isDivisible:
                dp[i] = max(dp[i], dp[j] + 1)
    print(max(dp))






    return


s = int(input())
solve(s)