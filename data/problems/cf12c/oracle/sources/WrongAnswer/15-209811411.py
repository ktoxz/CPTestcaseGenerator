n, m = map(int , input().split())
l = list(map(int , input().split()))
l1 = sorted(l , reverse= True)
l2 = sorted(l) 
d ={} 
for i in range(m) :
    s = input()
    if s not in d : 
        d[s] =1 
    else:
        d[s] += 1
print(d)
counter1 = 0
t = list(d.values())
for i in range(len(d)) : 
    mn = max(t)
    t.remove(mn)
    counter1 += mn * l2[i]
counter2 = 0 
t2 = list(d.values())
for i in range(len(d)) : 
    mx = max(t2)
    t2.remove(mx)
    counter2 += mx * l1[i]
print(counter1 , counter2)