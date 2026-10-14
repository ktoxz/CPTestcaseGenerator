from math import ceil
import math
from math import gcd
import bisect
# from math import lcm
from bisect import bisect_right
from itertools import combinations
from collections import Counter
# from operator import iand
# from math import log

ceil1 = lambda a,b: (a+b-1)//b
cubic_root = lambda n: round(math.exp(math.log(n)/3),6)
range_sum = lambda l,r: (l+r)*(r-l+1)//2




def get_sublists(lst):
    n = len(lst)
    sublists = []
     
    for start in range(n):
        for end in range(start + 1, n + 1):
            sublists.append(lst[start:end])
     
    return sublists


from collections import Counter
def get_prod(arr):
    ans =1
    for i in arr:
        ans*=i
    return ans


def get_distance(a1,b1):
    x1,y1 = a1[0],a1[1]
    x2,y2 = b1[0],b1[1]
    # if 

    dist = abs(x2-x1)+abs(y2-y1)
    return dist


def solve2(list_arr):
    n = len(list_arr)
    res = []
    for i in range(n-1):
        res.append(get_distance(list_arr[i],list_arr[i+1]))
    return sum(res)


def solve3(arr,n):
    ans = []
    for i in arr:
        ans.append(i[n])
    return ans

def solve():

    k = int(input())
    l = int(input())

    lg = math.log(l,k)
    st = str(lg)
    if st[-1]=='0':
        print('YES')
        print(int(lg)-1)
    else:
        print('NO')

(solve())