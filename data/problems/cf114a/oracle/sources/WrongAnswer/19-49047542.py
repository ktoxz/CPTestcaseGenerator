'''input
5
25
'''


import math


def primeFactors(n):

    s = []

    while n % 2 == 0: 
        n = n / 2
        s.append(2)
          
    # n must be odd at this point 
    # so a skip of 2 ( i = i + 2) can be used 
    for i in range(3,int(math.sqrt(n))+1,2): 
          
        # while i divides n , print i ad divide n 


        while n % i== 0: 
            n = n / i
            s.append(i)
              

    if n > 2: 
        s.append(n)

    return s

k = int(input())
l = int(input())

fac = primeFactors(l)
uniqFac = set(fac)

if uniqFac != {k}:
	print("NO")
else:
	print("YES")
	print(len(fac) - 1)