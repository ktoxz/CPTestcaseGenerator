import math
from decimal import * 
 
def functie_divizori(numar):
 
 
 dictionar={}
 
 matrice=[]
 if numar==1:
  a=[1]*2
  a.append(0)
  a.append(0)
  matrice.append(a)
 else: 
  for j in range(1,math.floor(numar**(1/2))+1):
  # print("j=",j)
   
   if numar%j==0:
    tupleta=[]
  #  print(dictionar)
    
 
     
 
     
     
    tupleta.append(j)
    tupleta.append(numar//j)
    tupleta.append(0)
    tupleta.append(0)
    matrice.append(tupleta)
    tupleta=[]
    
    if numar//j!=j:
     tupleta=[]
     tupleta.append(numar//j)
     tupleta.append(j)
     tupleta.append(0)
     tupleta.append(0)
   
  
     matrice.append(tupleta)
 return matrice
 

alfabet = {'a': 1, 'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,'g': 7,'h': 8,'i': 9,'j': 10,'k': 11,'l': 12,'m': 13,'n': 14,'o': 15,'p': 16,'q': 17,'r': 18,'s': 19,'t': 20,'u': 21,'v': 22,'w': 23,'x': 24,'y': 25,'z': 26}
alfabet_2={'1':"a", '2':"b", '3':"c", '4':"d", '5':"e", '6':"f", '7':"g", '8':"h", '9':"i", '10':"j", '11':"k", '12':"l", '13':"m", '14':"n", '15':"o", '16':"p", '17':"q", '18':"r", '19':"s", '20':"t", '21':"u", '22':"v", '23':"w", '24':"x", '25':"y", '26':"z"} 


  
def liber(vector,x,y,cate):
 answ=True
 
 for jj in range(y,y+cate):
  if jj<=k:
   if vector[x][jj]==1:
    answ=False
    break
  else:
   break
  
 return answ
 
 
def distanta(xx,yy,centrul,cate):
 
 return(abs(xx-centrul)+abs(yy+math.ceil((cate-1)/2)-centrul)*cate)
 
 
#cazuri=int(input())
 
#vector_a=list(map(int,input().split()))
#vector_b=list(map(int,input().split()))
 
#print(functie_divizori(2))
 
#for tt in range(cazuri):
 #print("tt=",tt)
 #n,x=map(int,input().split())
# bloc=list(map(int, input().split()))
#bloc.sort()
# bloc=bloc[::-1]
#print(functie_divizori(9))
 
n,k=map(int, input().split())
bloc=list(map(int, input().split()))



matrice = [[0 for _ in range(k+1)] for _ in range(k+1)]
#for i in range(k+1):
 #a=[]
 #for j in range(k+1):
#  a.append(0)
# matrice.append(a)
 
#print(matrice) 

centru=math.ceil(k/2)

for q in bloc:
#for p in range(1,1000):
# q=1
 minimul=2*k
 posibil=-1
 for i in range(k,0,-1):
  for j in range(k-q+1,0,-1):
   if liber(matrice,i,j,q):
    posibil=1
    d=distanta(i,j,centru,q)
    if minimul>=d:
     minimul=d
     rand=i
     yl=j
     yr=yl+q-1
   
 if posibil==-1:
  print(-1)
 else:
  #print(rand, end=' ')
  #matrice[rand][yl:yr+1]=1
  for z in range(yl,yr+1):
   
   matrice[rand][z]=1
  print(rand,yl,yr)

#print(bloc)