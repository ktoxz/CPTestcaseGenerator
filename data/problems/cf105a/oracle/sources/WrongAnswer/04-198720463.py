from math import floor

n, m, k = map(float, input().split())
skills = {}
for i in range(int(n)):
    name, exp = input().split()
    exp = int(exp)
    if exp >= 100:
        skills[name] = floor(exp * k)
for i in range(int(m)):
    name = input().strip()
    if name not in skills:
        skills[name] = 0

print(len(skills))
for name in sorted(skills):
    print(name, skills[name])