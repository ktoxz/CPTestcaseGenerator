n=input()
su=sum([int(i) for i in n])
if su%10==su:
    n=0
else:
    n=1
while su!=su%10:
    su=sum([int(i) for i in str(su)])
    n+=1
print(n)