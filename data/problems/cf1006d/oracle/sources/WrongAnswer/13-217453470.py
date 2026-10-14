n = int(input())
str1 = input()
str2 = input()

ans = 0
if n % 2:
    ans += (str1[n // 2] != str2[n // 2])

for i in range(0, n // 2):
    num = [0] * 27
    num[ord(str1[i]) - ord('a')] += 1
    num[ord(str2[i]) - ord('a')] += 1
    num[ord(str1[n - i - 1]) - ord('a')] += 1
    num[ord(str2[n - i - 1]) - ord('a')] += 1

    kind = 0
    flag = False
    for j in range(26):
        if num[j]:
            kind += 1
            if num[j] > 2:
                flag = True
    if kind == 2 and flag:
        ans += 1
    elif kind == 3:
        ans += (str1[i] == str1[n - i]) + 1
    elif kind == 4:
        ans += 2

print(ans)