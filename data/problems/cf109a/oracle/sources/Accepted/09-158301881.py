def is_sorted(arr,r=False):
    n=len(arr)
    if not r :
        for i in range(1,n):
            if arr[i]<arr[i-1] :
                return False
        return True
    else:
        for i in range(1,n):
            if arr[i]>arr[i-1] :
                return False
        return True


def freq(arr) :
    d={}
    for i in arr :
        d[i]=d.get(i,0)+1
    return d

def fac(n):
    p=1
    for i in range(1,n+1):
        p*=i
    return p



from functools import lru_cache


def check(s,n):
    sm=sum([int(x) for x in s])
    if sm==n :
        return s
    return -1

@lru_cache(maxsize=None)
def solve(n) :
    if n%7==0 :
        return check('7'*(n//7) , n )
    if n%7==1 :
        return check('4'*2 +'7'*(n//7-1) , n )

    if n%7==2 :
        return check('4'*4 + '7'*(n//7-2) , n )

    if n%7==3 :
        return check('4'*6 + '7'*(n//7-3) , n )
    if n%7==4 :
        return check('4'+'7'*(n//7) , n )
    if n%7==5 :
        return check('4'*3 + '7'*(n//7-1) , n )
    if n%7==6 :
        return check('4'*5 + '7'*(n//7-2) , n )

       












 



 
 


    


#from bisect import bisect_left as bisect
from math import ceil,floor
from sys import stdin #setrecursionlimit
input = stdin.buffer.readline    
#setrecursionlimit(400000)   



n=int(input())
print(solve(n))




'''

for _ in range(int(input())) :
    n=int(input())
    print(solve())


n=int(input())

x=input().strip().decode("utf-8")


n,m= list(map(int, input().split()))


n=int(input())
    arr=list(map(int, input().split()))

n,k= list(map(int, input().split()))
arr=list(map(int, input().split()))


arr=list(map(int, input().strip().decode("utf-8")))


n,m= [int(x) for x in input().split()]
arr=[list(map(int, input().split())) for _ in range(n)]


n,m= [int(x) for x in input().split()]
arr=[list(map(int, input().strip().decode("utf-8"))) for _ in range(n)]



n=int(input())
arr=[list(map(int, input().split())) for _ in range(n)]



n,m= list(map(int, input().split()))
    arr=[list(input().strip().decode("utf-8")) for _ in range(n)]




for _ in range(int(input())) :
    

    n=int(input())
    arr=list(map(int, input().split()))

    d={}
    leaves={}

    for i in range(n):
        d[i+1]=[]
        leaves[i+1]=1
    
    for i in range(1,n):
        d[arr[i-1]].append(i+1)
        if arr[i-1] in leaves :
            leaves.pop(arr[i-1])






'''