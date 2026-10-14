num1 = input()
length=len(num1)
num2=num1
num1=int(num1)
sum=0
i=0
count=0
while(num1>=10):
    while i<length:
        sum = sum + int(num2[i])
        i = i + 1
    count=count+1
    num1=sum
    sum=0
    if(num1<10):
        break
print(count)