Main = str(input().lower())
LM = len(Main)
Name = [""]
Num = [1]

for i in range(LM):
    for j in range(len(Name)):
        if(Main[i]==Name[j]):
            Num[j]+=1
            break
        if(Main[i]!=Name[j] and j==len(Name)-1):
            Name.append(Main[i])
            Num.append(1)

Count = 0
Max = 0
Word = []

for i in range(len(Num)):
    if(Num[i]>=4):
        Count += 1
        Word.append(Name[i]*4)

if(len(Word)==0):
    Word.append("")

print(Count)
for i in range(len(Word)):
    print(str(Word[i]))