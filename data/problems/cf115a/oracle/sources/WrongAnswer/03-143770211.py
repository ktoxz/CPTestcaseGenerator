n = int(input())
status = [0] * n
for i in range(n):
    status[i] = int(input())
s = [0] * n
manager = 0
for i in range(n):
    if status[i] != -1:
        s[status[i]] += 1
    else:
        manager = 1
counter = manager
for item in s:
    if item != 0:
        counter += 1
print(counter)