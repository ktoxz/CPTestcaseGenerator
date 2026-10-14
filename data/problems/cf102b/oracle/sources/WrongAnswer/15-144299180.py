n = int(input())
for r in range(n):
    x = int(input())
    x_str = str(x)
    items = []
    for i in range(len(x_str)):
        items.append(x_str[i])
    count = 0
    for i in items:
        count = count + int(i)
    print(count)