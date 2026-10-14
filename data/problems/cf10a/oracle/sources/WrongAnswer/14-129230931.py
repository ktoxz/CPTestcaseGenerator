n,  p1,  p2,  p3,  t1,  t2 = map(int, input().split())

lr = 1441
result = 0
for i in range(0,n):
    l, r = map(int, input().split())

    modo1 = t1 if (l - lr) >= t1  else (l - lr)
    modo2 = t2 if (l- lr - modo1) >= t2 else (l- lr - modo1)
    modo3 = (l - lr - modo1 - modo2)

    if (modo1 > 0):
        modo1 = modo1
    else:
        modo1 = 0
    
    if(modo1 > 0):
        modo2 = modo2
    else:
        modo2 = 0

    if(modo3 > 0):
        modo2 = modo2
    else:
        modo2 = 0

    result += (r-l) * p1+ modo1*p1 + modo2*p2 + modo3*p3
    lr = r

print(result)