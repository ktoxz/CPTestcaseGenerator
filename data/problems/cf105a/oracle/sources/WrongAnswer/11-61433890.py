skills = []
info = input().split()

N, M, K = int(info[0]), int(info[1]), float(info[2])

for i in range(N):
    name_exp = input().split()
    experience = int(name_exp[1])
    if experience * K >= 100:
        name_exp[1] = str(int(experience * K))
        skills.append(name_exp)

for i in range(M):
    name = input()
    inSkills = False
    for key in skills:
        if key[0] == name:
            inSkills = True
            break
    
    if inSkills == False:
        skills.append([name, '0'])

skills.sort()

print(len(skills))
for key in skills:
    print(key[0] + ' ' + key[1])