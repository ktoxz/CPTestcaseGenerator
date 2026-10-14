n=int(input())
res=int(input())
num=list(map(int,str(n)))
ans=list(map(int,str(res)))
num=sorted(num)
i=0
while num[i]==0:
    i+=1
    continue
num[0]=num[i]
num[i]=0 
if num==ans:
    print("OK")
else:
    print("WRONG_ANSWER")