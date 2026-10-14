n,d=map(int,input().split())
b=list(map(int,input().split()))
moves=0
for i in range(1,n):
    if b[i-1]>=b[i]:
        moves+= (b[i-1]-b[i])//d+1
        b[i]+=moves*d
print(moves)