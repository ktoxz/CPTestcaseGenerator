n, m = map(int, input().split())
prices = list(map(int, input().split()))
fruits = {}

for i in range(m):
    fruit = input()
    if fruit in fruits:
        fruits[fruit].append(prices[i])
    else:
        fruits[fruit] = [prices[i]]

min_total_price = 0
max_total_price = 0

for fruit, fruit_prices in fruits.items():
    min_price = min(fruit_prices)
    max_price = max(fruit_prices)
    min_total_price += min_price
    max_total_price += max_price

print(min_total_price, max_total_price)