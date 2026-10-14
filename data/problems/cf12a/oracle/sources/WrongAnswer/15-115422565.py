l=[]
for i in range(3):
    x=input()
    for each in x:
        l.append(each)
print(l)
p1,p2=0,8
while p1<p2:
    if l[p1]==l[p2]:
        p1=p1+1
        p2=p2-1
    else:
        print("NO")
        break
else:
    print("YES")