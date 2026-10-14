from sys import stdin; inp = stdin.readline
from math import dist, ceil, floor, sqrt, log
from collections import defaultdict, Counter, deque
def IA(sep=' '): return list(map(int, inp().split(sep)))
def QA(sep=' '): return deque(map(int, inp().split(sep)))
def FA(): return list(map(float, inp().split()))
def SA(): return inp().split()
def I(): return int(inp())
def F(): return float(inp())
def S(): return input()
def O(l:list): return ' '.join(map(str, l))

def main():
    n, p1, p2, p3, t1, t2 = IA()
    start = c =  0
    for i in range(n):
        l, r = IA()
        if i == 0:
            start = l
        c += (r-l)*p1 # normal work
        if l > start:
            # there is a brake 
            brake = l-start
            if brake > t1 and brake > t1+t2:
                p1_duration = t1
                p3_duration = brake - (t1+t2)
                p2_duration = brake - (p1_duration+p3_duration)
                # print(p1*p1_duration)
                c+= p1*p1_duration
                # print(p3*p3_duration)
                c+= p3*p3_duration
                # print( p2*p2_duration)
                c+= p2*p2_duration
                # print(f'brake: {brake},p1Dur: {p1_duration}, p2Dur: {p2_duration}, p3Dur: {p3_duration}')
            elif brake > t1:
                c+= t1*p1 
                c+= (brake-t1)*p2 
            else: 
                brake*p1 
        start = r
    return c
            
if __name__ == '__main__':
    print(main())