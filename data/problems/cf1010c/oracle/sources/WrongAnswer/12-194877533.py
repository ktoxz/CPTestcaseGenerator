for __ in range(1):
    n,k=map(int,input().split())
    a=list(map(int,input().split()))
    s=set()
    for i in range(len(a)):
        s.add(a[i]%k)
    e=list(s)
    for i in range(len(e)):
        for j in range(2,k):
            s.add((e[i]*j)%k)
    e=list(s)
    for i in range(len(e)):
        for j in range(i,len(e)):
            s.add((e[i]+e[j])%k)
    s=list(s)
    print(len(s))
    for i in s:
        print(i,end=" ")