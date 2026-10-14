n=int(input())
a=input()
b=input()
ans=0
for i in range(n//2):
    seen=set()
    seen.add(b[i])
    if b[n-i-1] in seen:
        seen.remove(b[n-i-1])
    else :
        seen.add(b[n-i-1])
    if a[i] in seen:
        seen.remove(a[i])
    else :
        seen.add(a[i])
    if a[n-1-i] in seen:
        seen.remove(a[n-i-1])
    else :
        seen.add(a[n-i-1])
    ans+=len(seen)
print(ans)