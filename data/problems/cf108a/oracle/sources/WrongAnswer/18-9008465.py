import sys
import math


h, m = [int(x) for x in (sys.stdin.readline()).split(':')]

if(h >= 0 and h < 5):
    h += 1
    print("0" + str(h) + ":" + str(h) + "0")
elif((h >= 11 and h < 15) or (h >= 21 and h < 23)):
    h += 1
    print(str(h) + ":" + str(h)[::-1])
elif(h == 5):
    print("11:11")
elif(h == 15):
    print("21:12")
elif(h == 23):
    print("00:00")