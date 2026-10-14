f = open("input.txt", mode="r")
entered, holding = f.read().split()
f.close()
result = {"front": "1", "back": "2"}
f = open("output.txt", mode="w")
if result[entered] == holding:
    f.write("L")
else:
    f.write("R")
f.close()