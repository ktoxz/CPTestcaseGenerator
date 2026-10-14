s = "0"

for _ in range(3):
    s+= input()


if all(s[i]==s[10-i] for i in range(1,5)):
    print("YES")
else:
    print("NO")