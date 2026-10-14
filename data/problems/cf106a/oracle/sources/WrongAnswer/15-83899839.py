tr = input()
t1,t2 = map(str,input().split())
g = ['A','K','Q','J','T']
if tr in t1 and tr not in t2:
    print('YES')
elif tr not in t1 and tr in t2:
    print('NO')
else:
    s1 = t1[0]
    s2 = t2[0]
    if s1 in g and s2 in g:
        l1 = g.index(s1)
        l2 = g.index(s2)
        if s1>s2:
            print('NO')
        else:
            print('YES')
    elif s1 in g:
        print('YES')
    elif s2 in g:
        print('NO')
    else:
        s1,s2 = int(s1),int(s2)
        if s1>s2:
            print('YES')
        else:
            print('NO')