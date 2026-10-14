a,b,n = map(int,input().split())
a1,b1,n1 = a,b,n
while n > 0:
    a,n = n,a%n
n1=n1-a
if n1<0:
    print(0)
while n1 > 0:
    b,n1 = n1, b%n1
if n1-b < 0:
    print(0)