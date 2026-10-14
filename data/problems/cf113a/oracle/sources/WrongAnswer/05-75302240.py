def isadj(str):
    if str[-4:] == 'lios':
        return 1
    elif str[-5:] == 'liala':
        return 2
    return 0


def isnoun(str):
    if str[-3:] == 'etr':
        return 1
    elif str[-4:] == 'etra':
        return 2
    return 0


def isverb(str):
    if str[-6:] == 'initis':
        return 1
    elif str[-6:] == 'inites':
        return 2
    return 0


def isPetyaLanguage():
    instr = input()
    strs = instr.split()
    flag = 0
    for i in range(0, len(strs)):
        if isadj(strs[i]):
            if flag == 0:
                flag = isadj(strs[i])
            elif flag != isadj(strs[i]):
                print('NO')
                return
        elif isverb(strs[i]):
            print('NO')
            return
        elif isnoun(strs[i]):
            if flag != isnoun(strs[i]) and flag != 0:
                print('NO')
                return
            if flag == 0:
                flag = isnoun(strs[i])
            break
    for j in range(i + 1, len(strs)):
        if (not isverb(strs[i])) or isverb(strs[i]) != flag:
            print('NO')
            return
    print('YES')


if __name__ == '__main__':
    isPetyaLanguage()