def function():
    file = open("input.txt", "r")
    file2 = open("output.txt", "w")
    door = file.readline().split("\n")[0]
    a = file.readline()
    if door == "front":
        file2.write("L" if a == "1" else "R")
    else:
        file2.write("L" if a == "2" else "R")
    file.close()
    file2.close()
    return file2


function()