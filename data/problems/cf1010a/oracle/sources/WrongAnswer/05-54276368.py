n = int(input());
mass  = int(input());
lift = list(map(int,input().split()))
land = list(map(int,input().split()))

arr = [0 for i in range(2*n+1)]
arr[0] = land[0];
j = 1
for i in range(n):
    index = n - i - 1;
    arr[j]=lift[index];
    j = j+1;
    arr[j]=land[index];
    j = j+1;
    
arr = arr[0:2*n]
#print(arr)

result = mass;
flag = True
for i in range(2*n):
    tmp = arr[i]-1;
    if(tmp == 0):
      flag = False;
      break;
    result = result + result/(tmp);
if(flag == True):
    if(result>1000000000):
        print(-1)
    else:
        print(result-mass)
else:
    print(-1)