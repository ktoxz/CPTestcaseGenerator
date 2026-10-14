f=open("input.txt","r")
o=open("output.txt","w")
s=f.readline()
n=f.readline()
if s=="front":
    if n=="1":
        o.write("L")
    else:
        o.write("R")
elif s=="back":
    if n=="1":
        o.write("R")
    else:
        o.write("L")