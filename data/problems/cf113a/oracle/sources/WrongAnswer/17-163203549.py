s=input().split()
m=['lios','etr','initis']
f=['liala','etra','inites']
q=s[0]
b=len(s)
x=-1
for i in m:
    o=q
    if len(o)>len(i):
        o=o[-len(i):]
    if o==i:
        x=1
        break
if x==-1:
    for i in f:
        o=q
        if len(o)>len(i):
            o=o[-1*len(i):]
        if o==i:
            x=0
            break
ans='YES'
if x==0:
    for j,i in enumerate(s):
        o='     '+i
        if o[-5:]==f[0]:
            s[j]=f[0]
            continue
        if o[-4:]==f[1]:
            s[j]=f[1]
            continue
        if o[-6:]==f[2]:
            s[j]=f[2]
            continue
        ans='NO'
        break
    if ans=='YES':
        o=s.count(f[1])
        if o != 1:
            ans='NO'
        else:
             y=s.index(f[1])
             for i in range(y):
                 if s[i] != f[0]:
                     ans='NO'
                     break
             if y+1 != b:
                 for i in range(y+1,b):
                     if s[i] != f[2]:
                         ans='NO'
                         break
    print(ans)    
elif x==1:
    for j,i in enumerate(s):
        o=' '*5+i
        if o[-4:]==m[0]:
            s[j]=m[0]
            continue
        if o[-3:]==m[1]:
            s[j]=m[1]
            continue
        if o[-6:]==m[2]:
            s[j]=m[2]
            continue
        ans='NO'
        break
    if ans=='YES':
        o=s.count(m[1])
        if o != 1:
            ans='NO'
        else:
            y=s.index(m[1])
            for i in range(y):
                if s[i] != m[0]:
                    ans='NO'
                    break
            if y+1 != b:
                for i in range(y+1,b):
                    if s[i] != m[2]:
                        ans='NO'
                        break
    print(ans)
else:
    print('NO')