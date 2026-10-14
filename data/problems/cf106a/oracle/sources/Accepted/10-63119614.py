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
#s = input()
##t = input()
#a = list(map(int, input().split()))
#print(l)
#c = list(map(int, input().split()))

#x1, y1, x2, y2 =map(int,input().split())
#n = int(input())
#f = []
#t = [0]*n
#f = [(int(s1[0]),s1[1]), (int(s2[0]),s2[1]), (int(s3[0]), s3[1])]
def larger(a, b):
    con = ["6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    p1 = 0
    p2 = 0
    for i in range(len(con)):
        if (a == con[i]):
            p1 = i
        if (b == con[i]):
            p2 = i
    return p1 > p2
#h = [""] * n
#f1 = sorted(f, key = lambda tup: tup[0])
t = input()
c1, c2 = input().split()
if ( c1[1] == t and not c2[1] == t):
    print("YES")
elif (not (c1[1] == c2[1])):
    print("NO")
elif (larger(c1[0], c2[0])):
    print("YES")
else:
    print("NO")
#f1 = sorted(t, key = lambda tup: tup[0])