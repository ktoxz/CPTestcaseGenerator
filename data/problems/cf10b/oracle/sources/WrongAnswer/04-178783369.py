n,k = map(int,input().split())
stage = [0]+[[k,0] for _ in range(k)]
k2 = (k+1)//2

for m in map(int,input().split()):
    y,x,score = 0,0,float('inf')
    for i in range(1,k+1):
        if stage[i][0]==k:
            temp = abs(i-k2)*m+(m//2)*((m+1)//2)
            if score>temp: score = temp; y = i; x = (k+1)//2-m//2
        else:
            if stage[i][0]>=m:
                temp = abs(i-k2)*m+m*(k-2*stage[i][0]+m)//2
                if score>temp: score = temp; y = i; x = stage[i][0]-m+1
            if stage[i][1]>=m:
                temp = abs(i-k2)*m+m*(k-2*stage[i][1]+m)//2
                if score>temp: score = temp; y = i; x = k-stage[i][1]+1
    if score<float('inf'): 
        print(y,x,x+m-1)
        if stage[y][0]==k: stage[y] = [(k-m)//2,(k-m+1)//2]
        elif x<stage[y][0]: stage[i][0] -= m
        else: stage[y][1] -= m
    else: print(-1)