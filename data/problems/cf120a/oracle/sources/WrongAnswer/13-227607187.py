f = open("input.txt", "r")
door = str(f.readline())[0:-1]
rail = int(str(f.readline()))
f.close()

if (door == "front" and rail == 1) or (door == "back" and rail == 0):
    out = "L"
else:
    out = "R"

f = open("output.txt", "w") 
f.write(out)