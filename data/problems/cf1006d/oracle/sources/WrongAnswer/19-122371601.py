for _ in range(1):
    n=int(input())
    st=input()
    rt=input()
    l=len(st)
    i=0
    j=l-1
    count=0
    while i <=j:
        if i==j:
            count =count +0 if st[i] ==rt[j] else count +1
        elif st[i] ==rt[i] and st[j] ==rt[j]:
            count +=0
        elif st[i] ==rt[j] and rt[i] ==st[j]:
            count +=0
        elif st[i] ==st[j] and rt[i] ==rt[j]:
            count +=0
        else:
            s=set()
            s.add(st[i])
            s.add(st[j])
            s.add(rt[i])
            s.add(rt[j])
            if len(s) ==2:
                count +=1
            elif len(s) ==3:
                if st[i] ==st[j] or rt[i] ==rt[j]:
                    count +=2
                else:
                    count +=1
            else:
                count +=2
        i+=1
        j-=1
    print(count)