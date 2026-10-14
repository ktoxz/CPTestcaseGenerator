s=input()
s+=input()
s+=input()
flag=True
for i in range(5):
    if(s[i]!=s[8-i]):
        flag=False
        break;
if flag:
    print("YES")
else:
    print("NO")