import sys
import math
from collections import Counter 
#from decimal import * 
import random 
 
 
alfabet = {'a': 1, 'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,'g': 7,'h': 8,'i': 9,'j': 10,'k': 11,'l': 12,'m': 13,'n': 14,'o': 15,'p': 16,'q': 17,'r': 18,'s': 19,'t': 20,'u': 21,'v': 22,'w': 23,'x': 24,'y': 25,'z': 26}
alfabet_2={'1':"a", '2':"b", '3':"c", '4':"d", '5':"e", '6':"f", '7':"g", '8':"h", '9':"i", '10':"j", '11':"k", '12':"l", '13':"m", '14':"n", '15':"o", '16':"p", '17':"q", '18':"r", '19':"s", '20':"t", '21':"u", '22':"v", '23':"w", '24':"x", '25':"y", '26':"z"}
 
 
def prime_generator(nr_elemente_prime):
 
 vector_prime=[-1]*nr_elemente_prime
 vector_rasp=[0]*nr_elemente_prime
 
 vector_prime[1]=1
 
 vector_rasp[1]=1
 #primes sieve 
 contor=2
 
 for i in range(2,nr_elemente_prime):
  if vector_prime[i]==-1:
   vector_prime[i]=1
   vector_rasp[contor]=i
   contor=contor+1
   for j in range(i+i,nr_elemente_prime,i):
    if vector_prime[j]==-1:
      vector_prime[j]=i
#print(i,j)
   
  
 #print(vector_rasp)
 set_prime=set(vector_rasp[2:len(vector_rasp)])
 set_prime.remove(0)
 return list(set_prime) 
 
 
def cautare(poz,tupleta,lungime):
 
 pornire=0
 oprire=poz-1
 
 
 centrare=(pornire+oprire)//2
 
# print("p=",pornire,"op=",oprire,"cen=",centrare)
 
 while pornire+1<oprire:
  centrare=(pornire+oprire)//2
  while tupleta[centrare][2]>tupleta[poz][1] and pornire+1<oprire:
   oprire=centrare
   centrare=(pornire+oprire)//2
   
  while tupleta[centrare][2]<=tupleta[poz][1] and pornire+1<oprire:
   pornire=centrare
   centrare=(pornire+oprire)//2
 
# print("cen=",centrare,pornire,oprire)
 if tupleta[centrare][2]>tupleta[poz][1]:
  centrare-=1
  
 else:
  if centrare+1<lungime:
   if tupleta[centrare+1][2]<=tupleta[poz][1]:
    centrare+=1
 return centrare
 
dictionar_linii={}
dictionar_coloane={}
 
#z=int(input()) 
for contorr in range(1):
 # empty_line=input()
 n=int(input())
 #n=1100
 #k=int(input())
 #n,k=list(map(int, input().split()))
 #stringul=input()
 #bloc=list(map(int, input().split()))
 #bloc=input()
 #bloc=[]
 #n=200000
 
 #lista=prime_generator(500000)
 n=abs(n)
 #print(len(lista))
 
 triunghi=math.ceil((((8*n+1)**(1/2)-1))/2)
 #print(triunghi)
 
 #cate=triunghi
 while ((triunghi+1)*triunghi//2-n)%2==1:
  triunghi+=1
 
 print(triunghi)