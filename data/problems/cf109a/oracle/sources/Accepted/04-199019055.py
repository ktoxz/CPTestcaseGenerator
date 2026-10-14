num = int(input())

count7 = 0
count4 = 0

while num >= 28 or (num % 4 != 0 and num > 4):
    num -= 7
    count7 += 1

while num >= 4:
    num -= 4
    count4 += 1

if num != 0:
    print(-1)
else:
    print("4" * count4 + "7" * count7)