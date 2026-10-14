num = list(map(int, input()))
total = curr = 0

for i in num:
    if not i % 3:
        total += 1
        curr = 0
    else:
        curr *= 10
        curr += i

        if not curr % 3:
            total += 1
            curr = 0

print(total)