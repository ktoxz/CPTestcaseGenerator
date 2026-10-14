from collections import Counter
n , m = map(int , input().split())
r = lambda : list(map(int, input().split()))
arr = r()
x = [input() for _ in range(m)]

fruit = Counter(x)
arr.sort()

a = 0
b = 0

for i,j in zip(list(fruit.values())[::-1] , arr):
    # print(i , j)
    a += i * j

arr = arr[::-1]
for i,j in zip(list(fruit.values())[::-1] , arr):
    # print(i , j)
    b += i * j

print(a , b)