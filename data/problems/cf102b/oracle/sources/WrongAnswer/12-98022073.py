import sys

n = list(input())
print(n)
count = 0
for i in range(len(n)):
    n[i] = int(n[i])
print(n)
if len(n) == 1:
    print(count)
    sys.exit()
while True:
    for i in range(len(n)):
        n[i] = int(n[i])
    sum1 = sum(n)
    print(sum1)
    if sum1 >= 10:
        count += 1
        print("count:         ", count)
        n.clear()
        sum1 = str(sum1)
        n = list(sum1)
        print('n', n)
    else:
        print(count+1)
        break