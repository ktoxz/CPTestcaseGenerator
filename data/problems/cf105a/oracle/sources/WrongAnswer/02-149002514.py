"""Transmigration"""


from traceback import print_tb


def main():
    n, m, k = map(float, input().split())
    skill_set = list(input().split() for _ in range(int(n)))
    names = []
    for i in range(len(skill_set) - 1, -1, -1):
        skill_set[i][1] = int(int(skill_set[i][1]) * k)
        if skill_set[i][1] <= 100:
            del skill_set[i]
    for i in skill_set:
        names.append(i[0])

    for j in range(int(m)):
        new_skill = input()
        if not (new_skill in names):
            skill_set.append([new_skill, 0])
    print(len(skill_set))
    for _ in sorted(skill_set):
        print(f"{_[0]} {_[1]}")
if __name__ == '__main__':
    main()