A,B,N=int(input()),int(input()),1
while A**N<B: N+=1
if A**N==B: 
    print("YES"),print(N-1)
else: 
    print("NO")