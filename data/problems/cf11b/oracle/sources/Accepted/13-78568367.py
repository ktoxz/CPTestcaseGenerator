n=abs(int(input()))
s,c,i=0,0,1
while(s<n or (s-n)%2==1):
    s=s+i
    i=i+1
    c=c+1
print(c)