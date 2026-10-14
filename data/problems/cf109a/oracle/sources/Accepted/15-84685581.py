n = int(input())
a,b = divmod(n,7)
c,d = divmod(b,4)
if a<d:
    print(-1)
else:
    print("4"*(c+2*d) + "7"*(a-d))