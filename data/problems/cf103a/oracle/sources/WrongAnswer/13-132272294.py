n=int(input())
s=0
l=list(map(int,input().split()))
penalty=(sum(l)-l[0])-(n-1)
clicks=sum(l)+penalty
print(clicks)