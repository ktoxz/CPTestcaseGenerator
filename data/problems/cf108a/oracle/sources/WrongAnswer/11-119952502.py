n=input()
if n[:2]=="23":
    print("00:00")
else:
    a=int(n[:2])
    print(str(a+1)+":"+str(a+1)[::-1])