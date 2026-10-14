n=int(input())
a=input()
b=input()
ans=0
for i in range((n-1)//2+1):
  if n%2==1 and i==(n-1)//2:
    if a[i]!=b[i]:
      ans+=1
  else:
    if (a[i]==b[i] and a[n-i-1]) or (a[n-i-1]==b[i] and a[i]==b[n-i-1]):
      continue
    elif a[i]==b[i] or a[i]==b[n-i-1] or a[n-i-1]==b[i] or a[n-i-1]==b[n-i-1]:
      ans+=1
    else:
      ans+=2
print(ans)