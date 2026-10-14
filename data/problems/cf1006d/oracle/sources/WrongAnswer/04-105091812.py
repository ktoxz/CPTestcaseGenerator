n= int(input())
a=input()
b=input()
ans=0
if n%2==0:
    i2=n//2
else:
    i2=n//2+1
for i in range(i2):
    if i==i2-1:
        if n%2!=0:
            if a[i]!=b[i]:
                ans+=1
        else:
            ans1=0
            s1=[a[i],a[n-i-1],b[i],b[n-i-1]]
            d=dict()
            for j in s1:
                if j not in d:
                    d[j]=1
                else:
                    d[j]+=1
            for j in d:
                ans1+=d[j]//2
            if ans1==0:
                ans+=2
            elif ans1==1:
                ans+=1
    else:
        ans1=0
        s1=[a[i],a[n-i-1],b[i],b[n-i-1]]
        d=dict()
        ans2=0
        for j in s1:
            if j not in d:
                d[j]=1
            else:
                d[j]+=1
        for j in d:
            ans1+=d[j]//2
            if ans2<d[j]:
                ans2=d[j]
        if ans1==0:
            ans+=2
        elif ans1==1 and (s1[0]==s1[1] or s1[2]==s1[3]) and ans2==2:
            ans+=2
        elif ans1==1:
            ans+=1
print(ans)