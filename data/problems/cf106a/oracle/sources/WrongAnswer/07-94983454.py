s=input('')
s1=input('')
a,b=s1.split(' ')
l=["6","7","8","9","T","J","Q","K","A"]
if((a[1]==b[1] and l.index(a[0])>l.index(b[0])) or a[1]==s):
    print('YES')
else:
    print('NO')