from collections import Counter

n,m = map(int,input().split())
prices = list(map(int,input().split()))
fruits = []

for i in range(m):
    fruit = str(input())
    fruits.append(fruit)

freq = Counter(fruits)
prices = sorted(prices)

maximum = 0
minimum = 0

freq.most_common()

i = 0

for fruit in freq:
    maximum += freq[fruit] * prices[~(i)]
    minimum += freq[fruit] * prices[i]

    i += 1
        
ans = [minimum, maximum]
    
for i in ans:
    print(i,end=' ')