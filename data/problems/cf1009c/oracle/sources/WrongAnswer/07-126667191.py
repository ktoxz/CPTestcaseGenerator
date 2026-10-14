import sys
 
p2D = lambda x: print(*x, sep="\n")
def II(): return int(sys.stdin.buffer.readline())
def MI(): return map(int, sys.stdin.buffer.readline().split())
def LI(): return list(map(int, sys.stdin.buffer.readline().split()))
def LLI(rows_number): return [LI() for _ in range(rows_number)]
def BI(): return sys.stdin.buffer.readline().rstrip()
def SI(): return sys.stdin.buffer.readline().rstrip().decode()
def li(): return [int(i) for i in input().split()]
def lli(rows): return [li() for _ in range(rows)]
def si(): return input()
def ii(): return int(input())
def ins(): return input().split()


n,m=MI()
posf=(n-1)/2
if(n%2!=0):
    negf=((n//2)*(n//2+1))/n
else:
    negf=((n//2)*(n//2-1)+n//2)/n
ans=0
for i in range(m):
    x,d=MI()
    ans+=x
    if(d>=0):
        ans+=posf*d
    else:
        ans+=negf*d
print(ans)