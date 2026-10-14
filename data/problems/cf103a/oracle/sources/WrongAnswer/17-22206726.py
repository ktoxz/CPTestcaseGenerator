x = input()
y = input().split()
count = 0
for i in range(0,int(x)):
    if int(y[i]) == 1:
        count += 1
    else:
        count += int(y[i])+i
print(count)