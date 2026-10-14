n,m = list(map(int,input().split()))
mat = []
d = {}
for _ in range(m):
    u,v,dist = list(map(int,input().split()))
    x = str(u)+':'+str(v) 
    d[x] = dist
    flag = 0
    for i in range(len(mat)):
        temp = mat[i]
        f,l = temp[0],temp[-1]
        if v==f:
            temp = [u]+temp
            flag = 1
            mat[i] = temp
            break
        elif u==l:
            temp.append(v)
            flag = 1
            mat[i] = temp
            break
    if flag==0:
        mat.append([u,v])
ans = []
for i in mat:
    if len(i)>=2 and i[0]!=i[-1]:
        ans.append(i)
mat = []
for i in ans:
    if mat==[]:
        mat.append(i[::])
    else:
        af,al = i[0],i[-1]
        flag = 0
        for j in range(len(mat)):
            f,l = mat[j][0],mat[j][-1]
            if l==af:
                mat[j] = mat[j]+i[1::]
                flag = 1
                break
            elif f==al:
                mat[j] = i[::]+mat[j][1::]
                flag = 1
                break
        if flag==0:
            mat.append(i)
print(len(mat))
# print(mat)
for i in mat:
    t = 10**10
    prev = i[0]
    for j in range(1,len(i)):
        cur = i[j]
        x = str(prev)+':'+str(cur)
        t = min(t,d[x])
        prev = cur
    print(i[0],i[-1],t)