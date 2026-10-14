file = open("input.txt","r")
file2 = open("output.txt","w")
door = file.readline().split("\n")[0]
a = file.readline()
print(a)
if door == "front":
    file2.write("L" if a == 1 else "R")
else:
    file2.write("L" if a == 2 else "R")