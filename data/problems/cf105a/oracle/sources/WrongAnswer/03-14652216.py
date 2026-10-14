curNewSkillCo = input().split(" ")
cnsc = curNewSkillCo[:]
majorListParallel1 = []
majorListParallel2 = []
majorListNew1 = []
majorListNew2 = []
cnsc[0] = int(cnsc[0])
cnsc[1] = int(cnsc[1])
cnsc[2] = float(cnsc[2])
for i in range(cnsc[0]):
    aList = input().split(" ")
    aList[1] = int(aList[1])
    majorListParallel1.append(aList[0])
    majorListParallel2.append(aList[1])
for i in range(cnsc[1]):
    newSkill = input()
    majorListNew1.append(newSkill)
    majorListNew2.append(0)
#input is done time for processing
i = 0
while i < len(majorListParallel2):
    majorListParallel2[i] = majorListParallel2[i] * cnsc[2]
    if majorListParallel2[i] < 100:
        majorListParallel2.pop(i)
        majorListParallel1.pop(i)
        i -= 1
    i += 1
list1 = majorListNew1[:]
list2 = majorListNew2[:]
majorListNew1 += majorListParallel1
majorListNew2 += majorListParallel2
majorListParallel1 += list1
majorListParallel2 += list2
for item in majorListParallel1:
    if majorListParallel1.count(item) > 1:
        index2 = majorListNew1.index(item)
        majorListNew1.pop(index2)
        majorListNew2.pop(index2)
dict1 = {}
for item in majorListNew1:
    dict1.update({majorListNew1.index(item) : item})
majorListNew1.sort()
dict2 = {}
for item in majorListNew1:
    dict2.update({item : majorListNew1.index(item)})
indexList = majorListNew2[:]
for i in range(len(majorListNew2)):
    movedValue = dict1[i]
    indeces = dict2[movedValue]
    majorListNew2[indeces] = indexList[i]
for i in range(len(majorListNew2)):
    majorListNew2[i] = int(majorListNew2[i])
    majorListNew2[i] = str(majorListNew2[i])
print(len(majorListNew1))
for i in range(len(majorListNew1)):
    print(majorListNew1[i], majorListNew2[i])