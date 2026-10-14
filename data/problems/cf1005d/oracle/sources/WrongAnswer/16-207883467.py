num = input()

cur = 0
ans = 0

for n in num:
    d = int(n)
    if not d % 3:
        cur = 0
        ans += 1
    else:
        cur = (cur + d) % 3
        if not cur:
            ans += 1

print(ans)