list1 = input().split()
n = int(list1[0])
m = int(list1[1])
k = float(list1[2])
dic1 = {}


for i in range(n):
    key1, value1 = input().split()
    value1 = int(value1) * k
    if value1 > 100:
        dic1[key1] = round(value1)

for j in range(m):
    key2 = input()
    if key2 not in dic1.keys():
      dic1[key2] = 0


for x in sorted(dic1):
    print(x, dic1[x])