#import math
#n, m = input().split()
#n = int (n)
#m = int (m)
#n, m, k = input().split()
#n = int (n)
#m = int (m)
#k = int (k)
#n = int(input())
#m = int(input())
s = input()
##t = input()
#a = list(map(int, input().split()))
#print(l)
#c = list(map(int, input().split()))

#x1, y1, x2, y2 =map(int,input().split())
#n = int(input())
#f = []
#t = [0]*n
#f = [(int(s1[0]),s1[1]), (int(s2[0]),s2[1]), (int(s3[0]), s3[1])]

#h = [""] * n
#f1 = sorted(f, key = lambda tup: tup[0])
n =int( s[0:2])
m = int(s[3:])
m += 1
if m == 60:
    m = 0
    n += 1
    if n == 24:
        n = 0
while (True):
        a = n //10
        b = n % 10
        c = m // 10
        d = m % 10
        if (a == d and b == c):
            break
        else:
            m += 1
            if m == 60:
                m = 0
                n += 1
                if n == 24:
                    n = 0
if (n == 0 and m == 0):
    s = str(0)+str(0)+":"+str(0)+str(0)
elif(n == 0):
    s = str(0)+str(0)+":"+str(m)
elif(m == 0):
    s = str(n)+":"+str(0)+str(0)
else:
    s = str(n)+":"+str(m)
print(s)
#f1 = sorted(t, key = lambda tup: tup[0])