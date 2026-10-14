h=input()
c=""
ans=""
for i in h:
    if i.isdigit():
        c+=i
n1=int(c[:2])
n2=int(c[2:])
n3=str(n1+1)
ans=(n3)+":"+(n3[::-1])
if h=="23:59":
    print("00:00")

else:print(ans)