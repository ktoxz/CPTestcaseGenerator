z,m=map(int,input().split(':'))
s=str([(z+1)%24,20][z/5==3])
print(s+':'+s[::-1])