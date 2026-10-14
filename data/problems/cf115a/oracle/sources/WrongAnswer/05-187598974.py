def Dfs(source):
    stack=[source]
    depth=[0]*x
    maxdepth=0
    vis = [False]*x
    while len(stack)>0:
        i = stack.pop()
        if vis[i]:continue
        vis[i]=True
        for v in adj[i]:
            if not vis[v]:
                 stack.append(v)
                 depth[v]+=depth[i]+1
                 maxdepth=max(depth[v],maxdepth)
    return maxdepth
x=int(input())
adj = [[] for i in range(x)]
for i in range(x):
    adj[int(input())-1].append(i)
groups=0
for i in range(x):
    groups =max(Dfs(i),groups)
print(groups)