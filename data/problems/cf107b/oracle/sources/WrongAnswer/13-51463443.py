n, m, sh = map(int, input().split())
arr=[int(i) for i in input().split()]
sh-=1
#
import sys
#
if arr[sh] == 1:
    print (-1)
    sys.exit()   #error
arr[sh]-=1
#print(arr)
#
from math import factorial as fak

def binom(n, k):
    x = fak(n)/(fak(k) * fak(n - k))
    return x
#
n -= 1
N = min(n, arr[sh])
Sum = sum(arr)
#print(N, ' ', n, ' ', Sum)
count = 0.0
for i in range(1, N + 1):
    #print(arr[sh], ' ' , i, ' ' , Sum - arr[sh], ' ', n - i)
    count += binom(arr[sh], i) * binom(Sum - arr[sh], n - i)
    #print(count)
count /= binom(Sum, n)
print(count)