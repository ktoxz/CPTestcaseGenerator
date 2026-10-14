line=input()
l=line.split()
a=int(l[0])
b=int(l[1])
n=int(l[2])
wn=0
op=0
while True:
                if n<=0:
                                break
                else:
                                if op==0:
                                                v=1
                                                if a>n:
                                                                gr=a
                                                else:
                                                                gr=n
                                                for hj in range(1,gr):
                                                                if a%hj==0 and n%hj==0:
                                                                                v=hj
                                                n=n-v
                                                wn=0
                                                op=1
                                else:
                                                v=1
                                                if b>n:
                                                                gr=b
                                                else:
                                                                gr=n
                                                for hj in range(1,gr):
                                                                if b%hj==0 and n%hj==0:
                                                                                v=hj
                                                n=n-v
                                                wn=1
                                                op=0
print(wn)