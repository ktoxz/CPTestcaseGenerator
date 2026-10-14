# №1.1 НОД
# a, b = map(int, input().split())
# while a != b:
#     if a < b:
#         b = b - a
#     else:
#         a = a - b
# print(a)

# №1.2 НОД
# a, b = map(int, input().split())
# while b > 0:
#     a, b = b, a % b
# print(a)

# №1.1 НОК
# a, b = map(int, input().split())
# ai = a
# bi = b
# while b > 0:
#     a, b = b, a % b
# NOK = (ai * bi)/a
# print(int(NOK))
#
# a, b = map(int,input().split())
# v = a * b
# while b > 0:
#     c = a % b
#     a = b
#     b = c
# s = v / a
# print(int(s))

# def nod(a, b):
#     while b > 0:
#         a, b = b, a % b
#     return a
#
#
# a, b = map(int, input().split())
# print(a * b // nod(a, b))

# №1.3 Апельсины и гости
# def nod(a, b):
#     while b > 0:
#         a, b = b, a % b
#     return a
#
#
# a, b = map(int, input().split())
# print(int((a * b // nod(a, b)) / a))

# №1.4 A. Эпическая игра (119A)
a, b, n = map(int, input().split())
def nod(a, b):
    while b > 0:
        a, b = b, a % b
    return a
count = 1
while n >= nod(a, n) and n>= nod(b, n):
    if count % 2 != 0:
        n = n - nod(a, n)
    else:
        n -= nod(b, n)
    count +=1
print(str(count % 2))