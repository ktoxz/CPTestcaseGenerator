import math
import sys
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp(): # one integer input
    return(int(input()))
def inlt(): # list input
    return(list(map(int,input().split())))
def insr(): # string input
    s = input()
    return(list(s[:len(s) - 1]))
def invr(): # muliple integer variables input
    return(map(int,input().split()))


n = inp()
ans = 0

def sum_digits(a):
  sum = 0
  while a > 0:
    sum += a % 10
    a = math.floor(a / 10)
  return sum

while n > 9:
  n = sum_digits(n)

print(n)