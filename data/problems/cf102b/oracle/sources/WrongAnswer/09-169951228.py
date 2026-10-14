n=input()
p=[]
sum1=0
sum2=0

for i in n:
    c=int(i)
    sum1=sum1+c
    # print(sum1)
    if(sum1==0):
        l=0
    else:
        l=1
while(sum1//10!=0):
    while(sum1>0):
        sum2=sum2+sum1%10
        sum1=sum1//10



    l+=1

# print(sum2)
# print("lll")
# print(sum1)
sum3=0
while(sum2//10!=0):
    while(sum2>0):
        sum3=sum3+sum2%10
        sum2=sum2//10

    l+=1


# print(sum3)
# print(l)
sum4=0
while(sum3//10!=0):
    while(sum3>0):
        sum4=sum4+sum3%10
        sum3=sum3//10

    l+=1
print(l)