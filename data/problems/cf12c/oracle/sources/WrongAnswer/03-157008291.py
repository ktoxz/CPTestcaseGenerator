import array
input_n_fruits = [None]*2
input_n_fruits = input().split()

prices_fruits = array.array('i',(0 for i in range(0,int(input_n_fruits[1]))))
name_fruits = [None] * int(input_n_fruits[1])
prices_fruits =  [ int(x) for x in input().split()]


for i in range(int(input_n_fruits[1])):
    name_fruits[i] = input()

prices_fruits.sort()
print(prices_fruits)

min = 0
max = 0
for i in range(int(input_n_fruits[1])):
    min = min + prices_fruits[i]
    max = max + prices_fruits[int(len(prices_fruits))-1-i]


print(min, max)