a,b=input().split(":")
a=int(a)
b=int(b)
l1=['00','01','02','03','04','05','06','10','11','12','13','14','15','20','21','22','23']
l2=['00','10','20','30','40','50','60','01','11','21','31','41','51','02','12','23','32']
for i in range(len(l1)):
    if(i<len(l1)-1 and int(l1[i])==a and int(l2[i])==b):
        print(l1[i+1],end="")
        print(":",end="")
        print(l2[i+1])
        break
    elif(i==len(l1)-1 and int(l1[i])==a and (int(l2[i])==b or int(l2[i])<b)):
        print(l1[0],end="")
        print(":",end="")
        print(l2[0])
        break
    elif(i<len(l1)-1 and int(l1[i])==a and int(l2[i])>b):
        print(l1[i],end="")
        print(":",end="")
        print(l2[i+1])
        break
    elif(i<len(l1)-1 and int(l1[i])==a and int(l2[i])<b):
        print(l1[i+1],end="")
        print(":",end="")
        print(l2[i+1])
        break
    elif(i==len(l1)-1 and int(l1[i])==a and int(l2[i])>b):
        print(l1[i],end="")
        print(":",end="")
        print(l2[0])
        break
    elif(int(l1[i])>a):
        print(l1[i],end="")
        print(":",end="")
        print(l2[i],end="")
        break