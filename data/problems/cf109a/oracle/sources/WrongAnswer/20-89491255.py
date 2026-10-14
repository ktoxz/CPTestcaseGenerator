a=int(input())
a1=4
a2=a-4
for i in range (0,a-4):
    if a1%4==0 and a2%7==0:
        print(('4'*(a1//4))+('7'*(a2//7)))
        exit()
    a1+=1
    a2-=1
print('-1')