import re

in1 = [int(x) for x in re.split("\\s", input())]
in2 = [int(x) for x in re.split("\\s", input())]

words = []
count = []

for x in range(in1[1]):
    inX = input()
    if inX not in words:
        words.append(inX)
        count.append(1)
    else:
        count[words.index(inX)] += 1

count.sort()
in2.sort()
y = 0
totalA = 0
totalB = 0
for x in count:
    totalA += x*in2[y]
    y += 1
    
y = 0
count.reverse()
in2.reverse()
for x in count:
    totalB += x*in2[y]
    y += 1
    
    
print(str(totalA) + " " + str(totalB))