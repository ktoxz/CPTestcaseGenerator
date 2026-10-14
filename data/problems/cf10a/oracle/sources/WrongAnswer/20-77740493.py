data_sets, p1, p2, p3, t1, t2 = map(int, input().split())
consum_work = 0
first_worked = []
last_worked = []
for i in range(data_sets):
    data = input().split()
    consum_work += (int(data[1]) - int(data[0]))*p1
    first_worked.append(int(data[0]))
    last_worked.append(int(data[1]))

del first_worked[0]
del last_worked[-1]
for i,j in zip(first_worked, last_worked):
    delta = abs(i - j)
    if delta == t1:
        consum_work += delta*p1
    elif t1 < delta <= t2:
        consum_work += t1*p1
        delta -= t1
        consum_work += delta*p2
    elif delta > t2:
        consum_work += t1*p1
        consum_work += t2*p2
        delta -= (t1 + t2)
        consum_work += delta*p3

print(consum_work)