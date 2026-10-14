checker = 0
output = 0
for  i in input():
    if int(i) % 3 == 0:
        output += 1
        continue
    
    checker += int(i)
    if checker % 3 == 0:
        output += 1
        checker = 0

print(output)