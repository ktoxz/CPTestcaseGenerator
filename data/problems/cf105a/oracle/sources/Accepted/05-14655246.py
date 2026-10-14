data = input().split()
old_count, new_count = map(int, data[0:2])
percent = int(data[2][2:])
skills = {}
for i in range(old_count):
    name, score = input().split()
    score = int(score) * percent // 100
    if score >= 100:
        skills[name] = score
for i in range(new_count):
    name = input().strip()
    if name not in skills:
        skills[name] = 0
print(len(skills))
for name, score in sorted(skills.items()):
    print(name, score)