info1 = input().split()
info2 = []
power = 0

for i in range(int(info1[0])):
    info2.append(input().split())

n = int(info1[0])
p1 = int(info1[1])
p2 = int(info1[2])
p3 = int(info1[3])
t1 = int(info1[4])
t2 = int(info1[5])
for i in range(n):
    info2[i][0] = int(info2[i][0])
    info2[i][1] = int(info2[i][1])

powerpminute = p1
totalmins = 0

for i in range(n):
    if i < n-1:
        powerpminute = p1
        power += (info2[i][1] - info2[i][0]) * powerpminute
        totalmins += info2[i][1] - info2[i][0]
        if t2 >= (info2[i + 1][0] - info2[i][0]) - totalmins >= t1:
            power += t1 * powerpminute
            powerpminute = p2
            power += ((info2[i + 1][0] - info2[i][0]) - totalmins - t1) * powerpminute
            totalmins += (info2[i + 1][0] - info2[i][0]) - totalmins
        elif (info2[i + 1][0] - info2[i][0]) - totalmins >= t2 >= t1:
            power += t1 * powerpminute
            powerpminute = p2
            power += ((info2[i + 1][0] - info2[i][0]) - totalmins - t1 - t2) * powerpminute
            powerpminute = p3
            power += ((info2[i + 1][0] - info2[i][0]) - totalmins - t1) * powerpminute
            totalmins += (info2[i + 1][0] - info2[i][0]) - totalmins
        else:
            totalmins += (info2[i + 1][0] - info2[i][0]) - totalmins
            power += ((info2[i + 1][0] - info2[i][0]) - totalmins) * powerpminute
    else:
        powerpminute = p1
        power += (info2[i][1] - info2[i][0]) * powerpminute
        break

print(power)