x = str(input(''))
lst = list(map(str, input().split()))
y = ["6", "7", "8", "9", "T", "J", "Q", "K","A"]
if lst[0][1]!=lst[1][1] and lst[0][1]!=x:
    print("NO")
elif lst[0][1]!=lst[1][1] and lst[0][1]==x:
    print('YES')
elif lst[0][1]==lst[1][1]:
    if y.index(lst[0][0])>y.index(lst[1][0]):
        print('YES')
    else:
        print('NO')