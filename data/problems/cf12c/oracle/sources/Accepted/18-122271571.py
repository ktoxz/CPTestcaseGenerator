n, bought = map(int, input().split())
price_list = sorted(list(map(int, input().split())))
fruit_count = {}
for i in range(bought):
    fruit = input()
    try:
        fruit_count[fruit] += 1
    except KeyError:
        fruit_count[fruit] = 1
order_by_most_bought = sorted(fruit_count, key=lambda x: fruit_count[x], reverse=True)
minSum = 0
maxSum = 0
for i in range(len(order_by_most_bought)):
    minSum += fruit_count[order_by_most_bought[i]]*price_list[i]
    maxSum += fruit_count[order_by_most_bought[i]]*price_list[-1-i]
print(minSum, maxSum)