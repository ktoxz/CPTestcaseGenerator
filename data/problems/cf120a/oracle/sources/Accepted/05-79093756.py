#ROUNIAAUDI
files=open("input.txt","r")
t,t1=files.read().split()
print(t,t1)
files.close()
files2=open("output.txt","w")
if t=="front" and t1=="1":
    files2.write("L")
elif  t == "front" and t1 == "2":
    files2.write("R")
elif  t == "back" and t1 == "2":
    files2.write("L")
elif  t == "back" and t1 == "1":
   files2.write("R")
files2.close()