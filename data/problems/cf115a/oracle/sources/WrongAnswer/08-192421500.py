n = int(input())  
g = 0
managers = []
for i in range(n):
    p = int(input())
    if p not in managers:  
        managers.append(p)
        g += 1
print(g)