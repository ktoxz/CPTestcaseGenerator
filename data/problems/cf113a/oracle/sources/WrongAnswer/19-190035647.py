s = input().split()
rules = ["lios","liala","etr","etra","initis","inites"]

for i in s:
    check=0
    for j in rules:
        if i[len(i)-len(j):len(i)]==j:
            check=1
    if check==0:
        print("NO")
        exit()
print("YES")