# cook your dish here
def find(l):
    sum=0
    for i in l:
        sum+=int(i)
    return sum
s=input()
l=list(s)
if(len(l)==1):
    print(0)
else:
    ans=0
    while 1:
        x=find(l)
        ans+=1
        if len(str(x))==1:
            break
        l=list(str(x))
        
    print(ans)