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
                #print('a')
        else:
            if a[i]==a[n-i-1] or b[i]==b[n-i-1]:
                if not (a[i]==b[i] and a[i]==b[n-i-1] and a[i]==a[n-i-1]):
                    ans+=1
                    #print('b')
            else:
                if not (a[i]==b[i] and a[n-i-1]==b[n-i-1])or (a[i]==b[n-i-1] and a[n-i-1]==b[i]):
                    if a[i]==b[i] or  a[n-i-1]==b[n-i-1] or a[i]==b[n-i-1] or b[i]==a[n-i-1]:
                        ans+=1
                        #print('c')
                    else:
                        #print('d')
                        ans+=2
    else:
        if a[i]==a[n-i-1] or b[i]==b[n-i-1]:
                if not (a[i]==b[i] and a[i]==b[n-i-1] and a[i]==a[n-i-1]):
                    ans+=1
                    #print('e')
        else:
            if not ((a[i]==b[i] and a[n-i-1]==b[n-i-1])or (a[i]==b[n-i-1] and a[n-i-1]==b[i])):
                if a[i]==b[i] or  a[n-i-1]==b[n-i-1] or a[i]==b[n-i-1] or b[i]==a[n-i-1]:
                    ans+=1
                    #print('f')
                else:
                    ans+=2
                    #print('g')
print(ans)