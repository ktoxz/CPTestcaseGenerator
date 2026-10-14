##n,m,k=map(int,input().split())
z=[x for x in input().split()]
keys={}
key=set()

for i in range (0,int(z[0])):
    a,b=input().split()
    keys[a]=int(b)
    keys[a]= float(z[2])*(int(b))
    if (keys[a]<100):
        del keys[a]
    else:
        key.add(a)

for j in range (0,int(z[1])):
    x=input()
    if x in keys.keys():
        pass
    else:
        key.add(x)
        keys[x]=0

key1=list(key)
key1.sort()
print (str(len(keys))+"\n")
for i in range (0,len(key1)):
    print (key1[i]+"\t"+str(int(keys[key1[i]])))