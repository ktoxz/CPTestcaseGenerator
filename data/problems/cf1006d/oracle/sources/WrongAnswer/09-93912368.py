n=int(input())
a=input()
b=input()
ans=0
for i in range((n-1)//2+1):
  if n%2==1 and i==(n-1)//2:
    if a[i]!=b[i]:
      ans+=1
  else:
    cost1=0
    if a[i]!=b[i]:
      cost1+=1
    if a[n-i-1]!=b[n-i-1]:
      cost1+=1
    cost2=0
    if a[i]!=b[n-i-1]:
      cost2+=1
    if a[n-i-1]!=b[i]:
      cost2+=1
    cost3=0
    if a[n-i-1]!=b[i]:
      cost3+=1
    if a[i]!=b[n-i-1]:
      cost3+=1
    ans+=min(cost1,cost2,cost3)
print(ans)