s = input()
a = s.find("AB")
b = s.find("BA")
if(abs(a-b)>=2 and (a!=-1 and b!=-1)):
    print("YES")
else:
    print("NO")