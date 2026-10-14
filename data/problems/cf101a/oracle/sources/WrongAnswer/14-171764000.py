from collections import Counter
 
variableS = input()
strLen = len(variableS)
variableN = int(input())
 
finalUniqueChar = 0
 
if (variableN > len(variableS)):
    print ("0")
else:
    myCounter = Counter(variableS)
    counterLen = len(myCounter)
    finalUniqueChar = counterLen
    #print (myCounter)
    #print (counterLen)
    if (counterLen == 1):
        print ("1")
        print (variableS)
    else:
        leastCommon = myCounter.most_common()[:-(counterLen+1):-1]
        #print (leastCommon)
        for letter in leastCommon:
            #print (letter[0], letter[1])
            if (letter[1] <= variableN):
                myCounter[letter[0]] = 0
                variableN = variableN - letter[1]
                finalUniqueChar = finalUniqueChar - 1
            else:
                break
           
        #print (myCounter)
 
        finalStr = ""
        for char in variableS:
            if (myCounter[char] != 0):
                finalStr = finalStr + char
        
        print (finalUniqueChar)
        print (finalStr)