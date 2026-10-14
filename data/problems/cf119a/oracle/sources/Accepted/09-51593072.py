def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)

def solve(a,b,n):
    turn=0
    while True:
        if turn%2==0:
            toPick=gcd(a,n)
            if n>=toPick:
                n-=toPick
            else:
                return 1 
        else:
            toPick=gcd(b,n)
            if n>=toPick:
                n-=toPick
            else:
                return 0 
        turn+=1


a,b,n=map(int,input().split())
print(solve(a,b,n))