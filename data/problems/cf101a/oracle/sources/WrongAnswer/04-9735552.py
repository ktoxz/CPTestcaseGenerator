kata=input()
k=int(input())
kat="abcdefghijklmnopqrstuvwxyz"
arr=[0]*26
for i in range(len(kata)):
    for j in range(26):
        if kata[i]==kat[j]:
            arr[j]+=1
            break
tot=0

for i in range(len(arr)):
    if(arr[i]>0):
        tot+=1
if(k>=len(kata)):
    print("0",end="\n")
    print()
elif(tot==1):
    print("1",end="\n")
    print(kata,end="\n")
else:
    karr=[]
    for i in range(26):
        karr+=[[i,arr[i]]]
    for i in range(26):
        for j in range(i+1,26):
            if(karr[i][1]<karr[j][1]):
                temp=karr[i]
                karr[i]=karr[j]
                karr[j]=temp
    tott=0
    m=0
    saring=""
    while(tott>-1 and m<25):
        m+=1
        if(tott>k):
            break
        elif(karr[m][1]>0):
            saring+=kat[karr[m][0]]
            tot=tot-1
            tott+=int(karr[m][1])
    output=""
    for i in range(len(kata)):
        status=True
        for j in range(len(saring)):
            if kata[i]==saring[j]:
                status=False
                break
            
        if status==True:
            output+=kata[i]

    print(tot,end="\n")
    print(output,end="\n")