h,m=map(int,input().split(":"))
if h==23 and m>=32:
    print("00:00");exit()
if m!=59:
    m+=1
if m==59:
    if h==23:
        h=00;m=00
    else:m=00
for i in range(1439):
    if str(h)==str(m)[::-1]:
        print(str(h)+":"+str(m));exit()
    else:m+=1