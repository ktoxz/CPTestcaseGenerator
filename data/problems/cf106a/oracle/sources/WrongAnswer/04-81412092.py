a = input()



b = input().split()

if  48<=ord(b[-1][0])<=57 and 48<=ord(b[0][0])<=57:


    if int(b[-1][0])> int((b[0][0])):
        if b[0][0]!=a:
            print('NO')
        else:
            print('YES')
    else:
        print('YES')
else:

    s=["6", "7", "8", "9", "T", "J", "Q", "K" ,"A"]
    if b[0][0]==a:
        if b[-1][0]==a:
            if s.index(b[0][0]) >= s.index(b[-1][0]):
                print('YES')
            else:
                print('NO')
        else:
            print('YES')
    else:
        if b[-1][0]==a:
            print('NO')
        else:
            if s.index(b[0][0]) >= s.index(b[-1][0]):
                print('YES')
            else:
                print('NO')