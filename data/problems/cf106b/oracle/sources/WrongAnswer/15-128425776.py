t = int(input())
speed = []
cost = []
while t:
    s,r,h,c = map(int,input().split())
    speed.append(s)
    cost.append(c)
    t -= 1
ans = 0
temp = 0
for i in range(len(speed)):
    diff = speed[i]-cost[i]
    if ans < diff:
        ans = diff
        temp = i
    
print(temp+1)