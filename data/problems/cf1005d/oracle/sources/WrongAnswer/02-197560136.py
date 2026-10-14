n = input()

ans = 0
s = ''

for ai in n: 
    s = ai + s
    if int(ai) % 3 == 0: 
        s = ''
        ans += 1
        continue
    for i in range(1, len(s)): 
        if int(s[:i]) % 3 == 0: 
            ans += 1
            s = ''
            break 

print(ans)