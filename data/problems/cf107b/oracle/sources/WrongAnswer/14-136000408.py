n,m,h = map(int,input().split())
L = list(map(int,input().split()))

import math
class GFG:
    def nCr(self, n, r):
        def gcd(a,b): # function to find gcd of two numbers in O(log(min(a,b)))
            if b==0: # base case
                return a
            return gcd(b,a%b)
        if r>n:
            return 0
        if r>n-r: # C(n,r) = C(n,n-r) better time complexity for lesser r value
            r = n-r
        mod = 10**9 + 7
        arr = list(range(n-r+1,n+1)) # array of elements from n-r+1 to n
        ans = 1
        for i in range(1,r+1): # for numbers from 1 to r find arr[j] such that gcd(i,arr[j])>1
            j=0
            while j<len(arr):
                x = gcd(i,arr[j])
                if x>1:
                    arr[j] //= x # if gcd>1, divide both by gcd
                    i //= x
                if arr[j]==1: # if element becomes 1, its of no use anymore so delete from arr
                    del arr[j]
                    j -= 1
                if i==1:
                    break # if i becomes 1, no need to search arr
                j += 1
        for i in arr: # single pass to multiply the numerator
            ans = (ans*i)%mod
        return ans
if sum(L)<n:
    print(-1)
    quit()
ob = GFG()
x = sum(L) - 1 
y = n-1 
z = ob.nCr(x,y)
w = ob.nCr(sum(L) - L[h-1],n-1)
t = (z - w)/(z)
v = math.ceil(t*10**6)/10**6
print(v)