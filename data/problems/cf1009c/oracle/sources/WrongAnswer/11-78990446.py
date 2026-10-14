n, changes = map(int, input().split())

answer = 0


def summation(n):
    return ((n - 1) * (n)) / 2


def negative_summation(n):
    if n % 2 == 1:
        weigth = summation(n // 2 + 1) * 2
    else:
        weigth = (summation((n // 2 + 1) - 1) * 2) + n // 2
    return weigth


negative_impact = negative_summation(n)
positive_impact = summation(n)

for change in range(changes):

    x, impact = map(int, input().split())

    answer += x * n

    if impact > 0:
        answer += impact * positive_impact
    else:
        answer += impact * negative_impact

print(answer/n)