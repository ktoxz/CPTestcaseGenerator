# Question: K - 3
# Assignment 7
# Daniel Perez, bd2255

def rainy(PRICE, FRUITS_QUANTITY, FRUITS):
    FINAL_MAX_COST = 0
    FINAL_MIN_COST = 0

    N = len(FRUITS)
    
    MIN_COST = PRICE[:N]
    PRICE.reverse()
    MAX_COST = PRICE[:N]

    X = list(FRUITS_QUANTITY.keys())
    X.sort()
    X.reverse()

    counter = 0
    for i in X:
        for j in FRUITS_QUANTITY[i]:
            FINAL_MIN_COST += i * MIN_COST[counter]
            counter += 1

    counter = 0
    for i in X:
        for j in FRUITS_QUANTITY[i]:
            FINAL_MAX_COST += i * MAX_COST[counter]
            counter += 1
    
    return FINAL_MIN_COST,FINAL_MAX_COST
    

RAW = input().split(' ')
N = int(RAW[0])
F = int(RAW[1])

RAW = input().split(' ')

PRICE = list(map(int, RAW))

PRICE.sort()

RAW = []
for i in range(F):
    X = input()
    RAW.append(X)
RAW_2 = dict()


for i in RAW:
    if not i in RAW_2:
        RAW_2[i] = 1
    else:
        RAW_2[i] += 1

FRUITS_QUANTITY = dict()
for i in RAW_2:
    if not RAW_2[i] in FRUITS_QUANTITY:
        FRUITS_QUANTITY[RAW_2[i]] = [i]
    else:
        FRUITS_QUANTITY[RAW_2[i]].append(i)

FRUITS = RAW_2

MIN, MAX = rainy(PRICE, FRUITS_QUANTITY, FRUITS)

print(str(MIN) + " " + str(MAX))