def solve() :
    if t==x[1]:
        return "YES"
    if t==y[1]:
        return "NO"
    d={"6":1, "7":2, "8":3, "9":4, "T":5, "J":6, "Q":7, "K":8 , "A":9}
    if d[x[0]]>d[y[0]]:
        return "YES"
    return "NO"




                    



 
from sys import stdin
input = stdin.readline     
    
 
t=input().strip()
arr=input().split()
x=arr[0]
y=arr[1]
print(solve())



'''

t=int(input())
for i in range(t) :
    print(solve())


n=int(input())

x=input().strip()


n,m= [int(x) for x in input().split()]




n=int(input())
arr=[int(x) for x in input().split()]


n,m= [int(x) for x in input().split()]
arr=[]
for i in range(n):
    arr.append([int(x) for x in input().split()])

n,m= [int(x) for x in input().split()]
arr=[]
for i in range(n):
    arr.append([x for x in input().strip()])


n=int(input())
arr=[]
for i in range(n):
    arr.append([int(x) for x in input().split()])


'''