n = list(map(int, list(input())))
ans = 0
N = []
fl = 0
for i in range(len(n)):
    if n[i] == 0:
        N.append(n[fl:i])
        fl = i + 1
        ans += 1

if fl < len(n):
    N.append(n[fl:])

for n in N:
    # print(n)
    use = [False] * len(n)
    rui = [0]
    for i in range(1, 6):
        for j in range(0, len(n) - i + 1):
            # print(n[j:j+i])
            if not any(use[j:j+i]):
                if sum(n[j:j+i]) % 3 == 0:
                    ans += 1
                    for s in range(j, j + i):
                        use[s] = True

print(ans)