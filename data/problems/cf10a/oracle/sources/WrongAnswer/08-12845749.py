import math

a = input().split()
k = 0
l = 0
n = math.ceil(int(a[0]))/2
o = []

for i in range(int(a[0])):
    b = input().split()
    c = int(b[1])-int(b[0])
    k += c
    o.append(int(b[0]))
    o.append(int(b[1]))

d = int(max(o)) - int(min(o))

def calc(k, d, l, n):
    l += int(a[1])*k
    shutdown = d - k
    if shutdown > 0:
        l += n * int(a[4]) * int(a[1])
        shutdown = shutdown - n * int(a[4])
        if shutdown > 0:
            l += n * int(a[5]) * int(a[2])
            shutdown = shutdown - n * int(a[5])
            if shutdown > 0:
                l += n * int(a[3]) * shutdown
    print(int(l))
                
                

calc(k, d, l, n)