from itertools import groupby

fruits = []
fruit_qty = []
answer_min = 0
answer_max = 0

price_tags, items = list(map(int, input().split()))
price = sorted(list(map(int, input().split())))

for _ in range(items):
  fruits.append(str(input()))

fruits.sort()
fruit_qty = [len(list(group)) for key, group in groupby(fruits)]
fruit_qty.sort(reverse = True)
#print(fruit_qty)

for i, j in zip(price, fruit_qty):
  answer_min += i * j

for i, j in zip(sorted(price, reverse=True), fruit_qty):
  answer_max += i * j

#print(price, fruits, fruit_qty, answer_min, answer_max)
print(answer_min, answer_max)

"""
fruits = []
shopping_cart = []
total_price = 0
a, b = list(map(int, input().split()))
price = list(map(int, input().split()))

for _ in range(b):
  fruits.append(str(input()))

low = sorted(price)
high = []

for price, fruit in zip(low, fruits):
  if fruit in shopping_cart:
    total_price = 0
    continue

  shopping_cart.append(fruit)


  if fruit in fruits:
    print(fruit, "orange asdas")
  print(price, fruit)



high = sum([i for i in sorted(price, reverse = True)[:b]])
low = sum([i for i in sorted(price)[:b]])
print(low, high)
"""