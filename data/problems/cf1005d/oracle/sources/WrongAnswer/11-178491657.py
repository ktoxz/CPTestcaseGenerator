nstr=input()
n=len(nstr)
dp=[0]*(n+1)
if int(nstr[0])%3==0:
    dp[1]=1
for i in range(2,n+1):
    for j in range(i):
        if i-j>1 and nstr[j]=='0':
            continue
        if int(nstr[j:i])%3==0:
            dp[i]=max(dp[i],dp[j]+1)
        else:
            dp[i]=max(dp[i],dp[j])
print(dp[n-1])