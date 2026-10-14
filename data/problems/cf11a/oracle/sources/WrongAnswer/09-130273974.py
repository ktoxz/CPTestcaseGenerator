n=input()
li=["4","7"]
c=0
l=len(n)
for i in n:
    if i in li:
        c+=1
if c==l:
    print("YES")
else:
    print("NO")