s = str(input())
count = 0
ans = ""
for j in range(len(s)):
    ans += s[j]
    if int(ans) % 3 == 0 or int(s[j]) % 3 == 0:
        count += 1
        ans = ""
print(count)