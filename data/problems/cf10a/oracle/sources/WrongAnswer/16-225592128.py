n, p1, p2, p3, t1, t2=map(int,input().split())
flag=False
w=0
last_shift=0
for _ in range(n):
    
    start,end=map(int,input().split())
    w=p1*(end-start)
    if n>1:
        
       if not flag:
            flag=True
       else:
           breaktime=start-last_shift
           w_t1=p1*(min(t1,breaktime))
           w_t2=p2*(min(t2,max((breaktime-t1),0)))
           w_t3 = p3 * max((breaktime - t1 - t2), 0)
           w+=w_t1+w_t2+w_t3
           last_shift=end
print(w)