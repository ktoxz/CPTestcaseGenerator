a, b = list(map(int, input().split()))
price = list(map(int, input().split()))

for _ in range(b):
  str(input())

high = sum([i for i in sorted(price, reverse = True)[:b]])
low = sum([i for i in sorted(price)[:b]])
print(low, high)