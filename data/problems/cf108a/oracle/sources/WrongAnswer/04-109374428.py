#!/usr/bin/env python
from __future__ import division, print_function
import math
import os
import sys
from sys import stdin,stdout
from io import BytesIO, IOBase
from collections import deque
#sys.setrecursionlimit(10**5)
if sys.version_info[0] < 3:
    from __builtin__ import xrange as range
    from future_builtins import ascii, filter, hex, map, oct, zip


# region fastio

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


def print(*args, **kwargs):
    """Prints the values to a stream, or to sys.stdout by default."""
    sep, file = kwargs.pop("sep", " "), kwargs.pop("file", sys.stdout)
    at_start = True
    for x in args:
        if not at_start:
            file.write(sep)
        file.write(str(x))
        at_start = False
    file.write(kwargs.pop("end", "\n"))
    if kwargs.pop("flush", False):
        file.flush()


if sys.version_info[0] < 3:
    sys.stdin, sys.stdout = FastIO(sys.stdin), FastIO(sys.stdout)
else:
    sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

input = lambda: sys.stdin.readline().rstrip("\r\n")
#-----------------------------------------------------------------

def regularbracket(t):
    p=0
    for i in t:
        if i=="(":
            p+=1
        else:
            p-=1
        if p<0:
            return False
    else:
        if p>0:
            return False
        else:
            return True

#-------------------------------------------------
def binarySearchCount(arr, n, key):
    left = 0
    right = n - 1

    count = 0

    while (left <= right):
        mid = int((right + left) / 2)

        # Check if middle element is
        # less than or equal to key
        if (arr[mid] <= key):
            count = mid+1
            left = mid + 1

        # If key is smaller, ignore right half
        else:
            right = mid - 1
    return count
# endregion
"""
def samesign(a,b):
    if (a>0 and b>0) or (a<0 and b<0):
        return True
    return False
def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int,input().split()))
        sum1=0
        l=[arr[0]]
        for i in range(len(arr)-1):
            if samesign(arr[i+1],arr[i])==True:
                l.append(arr[i+1])
            else:
              #  print(l)
               # print(max(l))
                sum1+=max(l)
                l=[arr[i+1]]
        #print(sum1)
       # print(l)
        sum1+=max(l)
        print(sum1)
"""
"""
def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int,input().split()))
        sum1 = sum(arr)
     #   max1 = max(arr)
        arr = sorted(arr)
        flag = True
        for i in range(1,n+1):
            if arr[i-1]>i:
                print("second")
                flag = False
                break
        if flag==True:
            diff = (n*(n+1))/2-sum1
            if diff%2==0:
                print("Second")
            else:
                print("First")
"""
"""
def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int,input().split()))
        seg = [0] * (n + 1)
        curr = 0
        cnt = 0
        for ai in a:
            if ai == curr:
                cnt += 1
            else:
                if cnt > 0:
                    seg[curr] += 1
                curr = ai
                cnt = 1
        if cnt > 0:
            seg[curr] += 1
        res = n
        for i in range(1, n + 1):
            if seg[i] == 0:
                continue
            op = seg[i] + 1
            if i == a[0]:
                op -= 1
            if i == a[-1]:
                op -= 1
            res = min(res, op)
        print((res))
"""
"""
def main():
    t = int(input())
    for _ in range(t):
        a,b = map(int,input().split())
        if a==0 or b==0:
            print(0)
        elif a>=2*b or b>=2*a:
            print(min(a,b))
        else:
            print((a+b)//3)
"""
"""
def main():
    t = int(input())
    for _ in range(t):
        n, m, x, y = map(int, input().split())
        ans = 0
        y = min(y, 2 * x)
        for i_ in range(n):
            s = input()
            i = 0
            while i < m:
                if s[i] == '*':
                    i += 1
                    continue
                j = i
                while j + 1 < m and s[j + 1] == '.':
                    j += 1
                l = j - i + 1
                ans += l % 2 * x + l // 2 * y
                i = j + 1
        print(ans)
"""
"""
def main():
    t = int(input())
    for _ in range(t):
        n,x = map(int,input().split())
        arr = list(map(int,input().split()))
        p=0
        sum1 = sum(arr)
        arr = sorted(arr)
        if sum1//n>=x:
            print(n)
        else:
            for i in range(n-1):
                sum1-=arr[i]
                if sum1//(n-(i+1))>=x:
                    print(n-(i+1))
                    break
            else:
                print(0)
"""
"""
def main():
    p = int(input())
    for _ in range(p):
        n,k = map(int,input().split())
        list1=[]
        if n==1 and k==1:
            print(0)
        else:
            for i in range(n,0,-1):
                if i+(i-1)<=k:
                    list1.append(i)
                    break
                else:
                    list1.append(i)
            list1.remove(k)
            print(len(list1))
            print(*list1)
"""
"""
def mirrortime(s):
    s = list(s)
    pp=""
    for i in range(len(s)):
        if s[i]=="0":
            continue
        elif s[i]=="2":
            s[i]="5"
        elif s[i]=="5":
            s[i]="2"
        elif i=="8":
            continue
        elif i=="1":
            continue
    for i in s:
        pp+=i
    return pp
#print(mirrortime("2255"))
def main():
    t = int(input())
    for _ in range(t):
        l=[3,4,6,7,9]
        h,m = map(int,input().split())
        s = input()
        t=s[0:2]
        p=s[3:5]
        ll=[]
        mm=[]
        t = int(t)
        p = int(p)
     #   print(t,p)
        for i in range(t,h):
            for j in range(p,m):
                i = str(i)
                if len(i)==1:
                    i="0"+i
                j = str(j)
                if len(j)==1:
                    j="0"+j
                if int(i[0]) in l or int(i[1]) in l or int(j[0]) in l or int(j[1]) in l:
                    continue
                else:
                    ll.append(i)
                    mm.append(j)
            p=0
     #   print(ll,mm)
        if len(ll)>=1:
            for i in range(len(ll)):
                cccc = ll[i]
                dddd = mm[i]
                ccc = mirrortime(cccc)
                ddd = mirrortime(dddd)
                ccc = list(ccc)
                ddd = list(ddd)
                ccc.reverse()
                ddd.reverse()
                ppp=""
                qqq=""
                for k in ccc:
                    ppp+=k
                for k_ in ddd:
                    qqq+=k_
                if int(qqq)<h and int(ppp)<m:
                   # print(int(qqq))
                   # print(int(ppp))
                    print(cccc+":"+dddd)
                    break
            else:
                print("00:00")

        else:
            print("00:00")
"""
"""
def main():
    n,x = map(int,input().split())
    cnt=0
    for _ in range(n):
        yn,ice = map(str,input().split())
        if yn=="+":
            x+=int(ice)
        else:
            x-=int(ice)
            if x<0:
                cnt+=1
                x+=int(ice)
    print(max(0,x),cnt)
"""
"""
def main():
    t = int(input())
    for _ in range(t):
        cnt=0
        l=[]
        s = input()
        if "1" not in s:
            print(0)
        else:
            cnt=0
            for i in s:
                if i=="0":
                    cnt+=1
                if i=="1":
                    l.append(cnt)
                    cnt=0
            if s[len(s)-1]!=1:
                l.append(cnt)
           # print(l)
            if s[0]=="0":
                l.remove(l[0])
            if s[len(s)-1]=="0":
                l.remove(l[len(l)-1])
            print(sum(l))
"""
"""
def main():
    d={}
    for i in range(26):
        d[chr(i+97)]=i
    for _ in range(int(input())):
        n, k = [int(s) for s in input().split()]
        s = input().strip()
        if n % k != 0:
            print(-1)
            continue
        pre = [[0 for i in range(26)] for j in range(n + 1)]
        for i in range(n):
            for j in range(26):
                pre[i][j] = pre[i - 1][j]
            pre[i][d[s[i]]] += 1
        for j in range(26):
            if pre[n - 1][j] % k != 0:
                break
        else:
            print(s)
            continue
        for i in range(n - 1, -1, -1):
            req = {}
            sumr = 0
            for j in range(26):
                if pre[i - 1][j] % k != 0:
                    req[chr(j + ord('a'))] = k - (pre[i - 1][j] % k)
                    sumr += (k - (pre[i - 1][j] % k))
            if sumr <= n - i and s[i] != 'z':
                if (n - i - sumr) % k == 0:
                    ans = s[:i]
                    flag = 0
                    if n - i - sumr > 0:
                        if chr(ord(s[i]) + 1) in req:
                            req[chr(ord(s[i]) + 1)] -= 1
                        else:
                            req[chr(ord(s[i]) + 1)] = k - 1
                            sumr += k
                        ans += chr(ord(s[i]) + 1)
                        flag = 1
                    req1 = sorted([[c, req[c]] for c in req])
                    if not flag:
                        for w in range(len(req1)):
                            if req1[w][0] > s[i]:
                                ans += req1[w][0]
                                req1[w][1] -= 1
                                flag = 1
                                break
                    if not flag:
                        continue
                    ans += "a" * (n - i - sumr)
                    for w in range(len(req1)):
                        ans += req1[w][0] * req1[w][1]
                    print(ans)
                    break
        else:
            print(-1)
"""
"""
def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int,input().split()))
        arr = sorted(arr)
        arr.reverse()
        cnt=0
        for i in range(n):
            if i%2==0:
                if arr[i]%2==0:
                    cnt+=arr[i]
            else:
                if arr[i]%2==1:
                    cnt-=arr[i]
        if cnt==0:
            print("Tie")
        elif cnt>0:
            print("Alice")
        else:
            print("Bob")
"""
"""
def main():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    q = list(map(int, input().split()))
    d = []
    c = 0
    for i in range(n):
        d.append(c + 1)
        c = c + a[i]
        d.append(c)
    print(d)
    for i in range(m):
        if q[i] == d[len(d) - 1]:
            print(len(d) // 2)
        else:
            print((binarySearchCount(d,len(d),q[i])+1)//2)
"""
def reverse(x):
    r=0
    while(x>0):
        rem=x%10
        r=r*10+rem
        x=x//10
    return r
def main():
    s = input()
    hr = s[0:2]
    mn = s[3:5]
    hr = int(hr)
    mn = int(mn)
    l=[]
    k=[]
    mn1 = mn+1
    for i in range(hr,24):
        for j in range(mn1,60):
            i = str(i)
            j = str(j)
            if len(i)==1:
                i="0"+i
            if len(j)==1:
                j="0"+j
            k = int(i+j)
            if k == reverse(k):
                print(i+":"+j)
                exit()
        mn1=0
    else:
        print("00:00")
if __name__ == '__main__':
    main()