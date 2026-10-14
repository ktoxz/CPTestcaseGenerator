import sys
import math
#from queue import *
import random
#sys.setrecursionlimit(int(1e6))
input = sys.stdin.readline
 
############ ---- USER DEFINED INPUT FUNCTIONS ---- ############
def inp():
    return(int(input()))
def inara():
    return(list(map(int,input().split())))
def insr():
    s = input()
    return(list(s[:len(s) - 1]))
def invr():
    return(map(int,input().split()))
################################################################
############ ---- THE ACTUAL CODE STARTS BELOW ---- ############

k=inp()
l=inp()
ans=-1
while l%k==0:
	l//=k
	ans+=1
if l==1:
	print("YES")
	print(ans)
else:
	print("NO")