n,p1,p2,p3,t1,t2=map(int,input().split())
arr=[]
power=0
for i in range(n):
    ok=tuple(map(int,input().split()))
    power += ((ok[1]-ok[0]) * p1)
    arr.append(ok)
for i in range(len(arr)-1):
    difference=arr[1][i]-arr[i][1]
    if difference-t1>=0:
        power+=t1*p1
        difference-=t1
    if difference-t2>=0:
        power+=t2*p2
        difference-=t2
    if difference>= 0:
        power += difference * p3
print(power)