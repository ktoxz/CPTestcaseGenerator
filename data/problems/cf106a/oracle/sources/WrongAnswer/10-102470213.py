t=input()
a,b=input().split()
d={'6':0,'7':1,'8':2,'9':3,'T':4,'J':5,'Q':6,'K':7,'A':8}
if(a[1]==t):
    print('YES')
elif(a[1]==b[1] and d[a[0]]>d[b[0]]):
    print('YES')
else:
    print('NO')