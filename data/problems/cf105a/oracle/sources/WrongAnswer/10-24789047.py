n, m, k = input().split()

n, m = int(n), int(m)
k = float(k)

skills = []
skill_set = set()
for _ in range(n):
    skill, val = input().split()
    val = int(val)
    if val >= 100:
        skill_set.add(skill)
        skills += [(skill, int(val * k))]

for _ in range(m):
    skill = input()
    if skill not in skill_set:
        skills += [(skill, 0)]

skills.sort()

print(len(skills))
for skill, val in skills:
    print(skill, val)