Main = int(input())
Mini = input().split()
Mana = 0
Count = 0

for i in range(Main):
    for j in range(int(Mini[i])):
        if(j==0 and i==0):
            Count+=1
        elif(j==int(Mini[i])-1):
            Count+=1
        else:
            Count+=1

if(len(Mini)%2==0):
    Count+=1

print(Count)