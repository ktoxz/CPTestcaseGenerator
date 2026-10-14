s = input()
z = 0
t = ""
for i in range(len(s)):
    if s[i] == "0" or int(s[i]) % 3 == 0:
        z += 1
        t += "0"
    else:
        t += s[i]

a = t.split("0")
num = 0
for i in range(len(a)):
    mod = -1
    q = 0
    for j in range(len(a[i])):
        k = int(a[i][j])
        if mod == -1:
            mod = k % 3
            q += 1
        else:
            mod += k % 3
            q += 1
        if mod % 3 == 0:
            num += 1
            mod = -1
            q = 0
        elif q == 3:
            num += 1
            mod = -1
            q = 0
print(z + num)