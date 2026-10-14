num = input()
n = len(num)
temp = 0
count = 0
for i in range(n - 1, -1, -1):
    if int(num[i]) % 3 == 0:
        count += 1
        temp = 0
        continue

    temp = int(num[i]) + temp
    if temp % 3 == 0:
        count += 1
        temp = 0
print(count)