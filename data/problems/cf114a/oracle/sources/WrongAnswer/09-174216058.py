from collections import defaultdict, deque
from functools import lru_cache
from heapq import heappush, heappop
from bisect import bisect_right, bisect_left

import math
hpop = heappop
hpush = heappush
MOD = 10**9 + 7
def solution():
    k = int(input())
    l = int(input())
    for i in range(1,31 + 1):
        if l == k**i:
            return print("YES")
    return print("NO")




def main():
    t = 1
    #t = int(input())
    for _ in range(t):
        solution() 
    
#import sys
#import threading
#sys.setrecursionlimit(1 << 30)
#threading.stack_size(1 << 27)
#thread = threading.Thread(target=main)
#thread.start(); thread.join()
main()
 
 
 
 
"""
"""