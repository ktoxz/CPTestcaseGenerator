from collections import deque
import sys
input = sys.stdin.readline
def bb(n):
    return [int(QQq) for QQq in '0'  *  (10 - len(bin(n)[2::])) + bin(n)[2::]]
def qw():
    return int(input())
def qq():
    return list(input())
def wq():
    return [int(xxxxx) for xxxxx in input().split()]
def bd(aaaaaa):
    qqq =0
    for i in range(len(aaaaaa)):
        qqq += 2 **( len(aaaaaa)- i -1) * aaaaaa[i]
    return qqq
def prost(n):
    i = 2
    while i *i <= n:
        if n  %  i == 0:
            return False 
        i +=1
    return True
def yy():
    print("YES")
def nn():
    print("NO")
al = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
yy()