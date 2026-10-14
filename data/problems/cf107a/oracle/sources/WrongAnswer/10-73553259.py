from collections import defaultdict

graph = defaultdict(list)
d = {}
n,m = list(map(int,input().split()))
for _ in range(m):
    u,v,dist = list(map(int,input().split()))
    x = str(u)+':'+str(v) 
    d[x] = dist
    graph[u].append(v)
visited = [False for i in range(n)]
mat = []
for i in range(n):
    # visited = [False for i in range(n)]

    if visited[i]==False:
        path = []
        st = i+1
        visited[i] = True
        q = [st]
        # path.append(st)
        while q!=[]:
            u = q[0]
            q.pop(0)
            path.append(u)
            f = 0
            for j in graph[u]:
                if visited[j-1]==False:
                    visited[j-1] = True
                    q.append(j)
                if j==st:
                    f = 1
                    break
            if f==1:
                break
                # else:
                #     path = []
                #     break
        if f==0:
            mat.append(path)
if mat==[]:
    print(0)
else:
    print(len(mat))
    for i in mat:
        ans = 10**10
        prev = i[0]
        for j in range(1,len(i)):
            cur = i[j]
            x = str(prev)+':'+str(cur)
            ans = min(ans,d[x])
            prev = cur
        print(i[0],i[-1],ans)