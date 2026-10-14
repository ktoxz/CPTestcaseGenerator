# LUOGU_RID: 128399015
a = input().split()
c = 5 #设置一个变量，记录当前的状态
for b in a:
    if c == 5:
        if len(a) == 1: 
            if b[-4:] == 'lios' or b[-5:] == 'liala' or b[-3:] == 'etr' or b[-4:] == 'etra' or b[-6:] == 'initis' or b[-6:] == 'inites': #输入只有一个任意合法单词时也特判为合法
                c = 0
        elif b[-4:] == 'lios':
            c = 1
        elif b[-5:] == 'liala':
            c = 2
        elif b[-3:] == 'etr':
            c = 3
        elif b[-4:] == 'etra':
            c = 4
        else:
            break
    elif c == 1:
        if b[-4:] == 'lios':
            continue
        elif b[-3:] == 'etr':
            c = 3
        else:
            c = 5
            break
    elif c == 2:
        if b[-5:] == 'liala':
            continue
        elif b[-4:] == 'etra':
            c = 4
        else:
            c = 5
            break
    elif c == 3:
        if b[-6:] == 'initis':
            c = 6
        else:
            c = 5
            break
    elif c == 4:
        if b[-6:] == 'inites':
            c = 7
        else:
            c = 5
            break
    elif c == 6:
        if b[-6:] == 'initis':
            continue
        else:
            c = 5
            break
    else:
        if b[-6:] == 'inites':
            continue
        else:
            c = 5
            break
if c in (1,2,5): 
    print('NO')
else:
    print('YES')