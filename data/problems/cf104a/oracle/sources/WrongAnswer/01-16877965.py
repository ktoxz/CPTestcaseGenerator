import sys
k = int(input())
if k>20 or k<=10:
    print("0")
    sys.exit()
k = k - 10
d = {1: 8, 2: 4, 3: 4, 4: 4, 5: 4,6: 4, 7:4, 8:4, 9:4, 10:15, 11:4}
print(d[k])