s=input('')
a,b=s.split(':')
a=int(a)
b=int(b)
if(a>=0 and a<=4):
    temp="0"+str(a+1)
    temp1=str(temp[::-1])
    list1=[temp,temp1]
    print(':'.join(list1))
elif(a>=5 and a<=9):
    print("10:01")
elif(a>=10 and a<=14):
    if(a==10 and b<2):
        print("10:01")
    else:
        temp2=str(a+1)
        temp3=str(temp2[::-1])
        list1=[temp2,temp3]
        print(':'.join(list1))
elif(a>=15 and a<=19):
    print("20:02")
elif(a>=20 and a<=22):
    if(a==20 and b<2):
        print("20:02")
    else:
        temp4=str(a+1)
        temp5=str(temp4[::-1])
        list1=[temp4,temp5]
        print(':'.join(list1))
else:
    print("00:00")