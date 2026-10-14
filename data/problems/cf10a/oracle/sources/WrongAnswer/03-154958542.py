import sys

val = []
out = 0
n,p1,p2,p3,t1,t2 = list(map(int,input().split()))

b = False
for s in sys.stdin:
    if(s == '\n'):
        break
    tmp = list(map(int,(s[:-1]).split()))
    out += (tmp[1]-tmp[0])*p1

    if(b):
        a = tmp[0]-val[1]
        if(a < t1):
            out += a*p1
            continue
        out += (t1)*p1
        a -= t1
        if(a < t2):
            out += a*p2
            continue
        out += (t2)*p2
        a -= t2
        out += a*p3
        
    val = tmp
    b = True
    
print(out)