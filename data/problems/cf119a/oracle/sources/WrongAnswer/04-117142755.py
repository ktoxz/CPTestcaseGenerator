# -*- coding: utf-8 -*-
"""
Created on Mon May 24 14:40:12 2021

@author: nagan
"""

a, b, n = map(int, input().split())
c = 0
ans = 9
while True:
    if c % 2 == 0:
        y = True
        d = min(a, n)
        if n < a:
            ans = 1
            break
        for i in range(d, 0, -1):
            if a % i == 0 and n % i == 0:
                n -= i
                y = False
                break
        if y == True:
            ans = 1
            break
        c += 1
    else:
        x = True
        d = min(b, n)
        if n < b:
            ans = 0
            break
        for i in range(d, 0, -1):
            if b % i == 0 and n % i == 0:
                n -= i
                x = False
                break
        if x == True:
            ans = 0
            break
        c += 1
print(ans)