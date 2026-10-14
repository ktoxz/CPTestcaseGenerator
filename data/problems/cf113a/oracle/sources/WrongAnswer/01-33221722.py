x=input()
i=0
b=True
while(i<len(x) and b):
  if(x[i]=="Q" or x[i] =="H" or x[i] =="9" or x[i] =="+"):
    b=False
  i+=1
if(b):
  print("NO")
else:
  print("YES")