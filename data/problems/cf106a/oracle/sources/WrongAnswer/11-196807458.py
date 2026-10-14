m = input()
c = input().split()
l1 = []
c1 = []
c2 = []
T, J, Q, K, A = 10, 11, 12, 13, 14
for i in c:
    l1.append(i)
for i in str(l1[0]):
    c1.append(i)
for i in str(l1[1]):
    c2.append(i)
if c1.count(m) == 1 and c2.count(m) == 0:
    print("YES")
if c1.count(m) == 1 and c2.count(m) == 1:
    if c1[0] > c2[0]:
        print("YES")
    else:
        print("NO")
if c1.count(m) == 0 and c2.count(m) == 0:
    if c1[0] > c2[0]:
        print("YES")
    else:
        print("NO")