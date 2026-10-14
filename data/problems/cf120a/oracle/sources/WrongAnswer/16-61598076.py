f1 = open("input.txt", 'r')
print(["L","R"][(f1.readline()=="front") ^ (int(f1.readline())==1)], end='')