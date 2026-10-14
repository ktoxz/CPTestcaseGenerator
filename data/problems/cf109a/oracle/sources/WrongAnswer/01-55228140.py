n = int(input())
ans = []
if (n%4==0):
    print((n//4%7)*'4' + ((n-(n//4%7))//7)*'7')
elif (n%7==0):
    print(n//7*'7')
elif(n%11==0):
    print(n//11*'4' + n//11*'7')
else:
    print(-1)