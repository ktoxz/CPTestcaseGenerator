t=int(input())
l=[];l2=[]
for _ in range(1):
    s1,r1,h1,c1=map(int,input().split())
    s=s1;r=r1;h=h1;c=c1
    l1=[s1,r1,h1,c1]
    l2.append(l1)
    while(t>1):
        s1,r1,h1,c1=map(int,input().split())
        l1=[s1,r1,h1,c1]
        l2.append(l1)
        if(s1>s and r1>r and h1>h and c1>c):
            s=s1;r=r1;h=h1;c=c1
        t-=1
m=1000;ans=0
for i in range(len(l2)):
    if(l2[i][0]>s or l2[i][1]>h or l2[i][2]>r or l2[i][3]>c):
        if(l2[i][3]<m):
            m=l2[i][3]
            ans=i
print(ans)