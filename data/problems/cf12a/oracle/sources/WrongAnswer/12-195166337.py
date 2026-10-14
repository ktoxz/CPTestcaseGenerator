arr=[]
for _ in range(3):
    arr1=list(map(str,input()))
    for i in arr1:
        if i=='X':
            arr.append(1)
        else:
            arr.append(0)
k=arr[::-1]
print(k,arr)
for i in range(9):
    if arr[i]!=k[i]:
        print('NO')
        exit()
print('YES')