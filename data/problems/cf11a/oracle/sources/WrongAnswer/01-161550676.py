n,d = list(map(int,input().split()))
lis = list(map(int,input().split()))
count = 0
for i in range(1,len(lis)):
    if lis[i-1] >= lis[i]:
        count += 1
print((len(lis)-len(set(lis)))+count)