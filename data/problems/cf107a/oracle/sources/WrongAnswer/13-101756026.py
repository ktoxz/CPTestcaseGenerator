import sys
input = sys.stdin.readline
for _ in range(1):
    n,m=[int(x) for x in input().split()]
    g,v=[[] for i in range(n)],[False for i in range(n)]
    for i in range(m):
        a,b,c=[int(x) for x in input().split()]
        g[a-1].append([b-1,c])
    ans=[]
    def helper(curr,start,dia):
        if len(g[curr])==0:
            ans.append([start+1,curr+1,dia])
            return
        for i in g[curr]:
            if v[i[0]]==False:
                v[i[0]]=True
                helper(i[0],start,min(dia,i[1]))
        return
    for i in range(n):
        if v[i]==False:
            v[i]=True
            helper(i,i,10000000000)
    print(len(ans))
    for i in ans:
        print(*i)