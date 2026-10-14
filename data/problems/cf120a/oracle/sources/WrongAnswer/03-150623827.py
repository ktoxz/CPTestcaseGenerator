import math
import sys
from decimal import *
from collections import deque
 
 
alfabet = {'a': 1, 'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,'g': 7,'h': 8,'i': 9,'j': 10,'k': 11,'l': 12,'m': 13,'n': 14,'o': 15,'p': 16,'q': 17,'r': 18,'s': 19,'t': 20,'u': 21,'v': 22,'w': 23,'x': 24,'y': 25,'z': 26}


 
#print(vector[9995:10001])

#c=int(input())

 
for i in range(0,1):
 #n=map(int,input().split())
 #n=int(input())
 #print(n,a,b)
 
 #lista=list(map(str,input().split()))
 sys.stdin=open("input.txt","r")
 sys.stdout=open("output.txt","w")
 
 stringul=[str(i) for i in sys.stdin.readline().split()]
 n=[int(i) for i in sys.stdin.readline().split()]

 
 
 if "front" in stringul and n==1 or stringul=="back" and n==2:
  print("L")
 else:
  print("R")
 #logul=int(math.log(n,10))
 
 
 

  
  
 
 
#print(rasp)