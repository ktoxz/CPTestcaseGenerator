n, m, h = map(int, input().split())
h -= 1
S = list(map(int, input().split()))


def solve():
    if sum(S) < n:
        return -1

    if sum(S) - S[h] < n - 1:
        return 1

    num1 = [k for k in range(1, sum(S) - S[h] + 1)]
    num2 = [k for k in range(1, sum(S) - n + 1)]
    den1 = [k for k in range(1, sum(S))]
    den2 = [k for k in range(1, sum(S) - S[h] - n + 2)]

    ans = 1

    for i in range(max(map(len, [num1, num2, den1, den2]))):
        ans *= num1[i] if i < len(num1) else 1
        ans *= num2[i] if i < len(num2) else 1
        ans /= den1[i] if i < len(den1) else 1
        ans /= den2[i] if i < len(den2) else 1

    return 1 - ans

print("%.12f\n" % solve())