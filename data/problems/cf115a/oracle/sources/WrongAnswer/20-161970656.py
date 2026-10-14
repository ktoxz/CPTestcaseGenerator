w=int(input())
l=[]
for i in range(w):
   
    t=int(input())
    l.append(t)
    l=set(l)
    l=list(l)
print(len(l))