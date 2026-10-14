import math
(n, m) = (int(i) for i in input().split())
array = [0]*n
result = 0
for i in range(m):
    (x, d) = (int(i) for i in input().split())
    mid = len(array)//2
    start = 0
    last  =len(array)-1
    # m = min(array[start], array[mid], array[last])
    index = 0
    if d<0:
        index = mid
    else:
        index = 0
    # index = array.index(m)
    result += x*len(array)
    if d<0:
        result+=(index)*(index+1)//2 *d + (len(array)-index-1)*(len(array) - index)//2*d
    else:
        result+=len(array)*(len(array)-1)/2*d
print("%.15f"%(result/len(array)))
    
# -2 1-4