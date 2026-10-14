n = int(input())
num = [int(i) for i in input().split()]
ans = 0


def re(n):
    if n == 1:
        return num[0]
    elif num[n-1] != 1:
        return re(n-1) + num[n-1] + n-1
    else:
        return re(n-1) + num[n-1]


print(re(n))