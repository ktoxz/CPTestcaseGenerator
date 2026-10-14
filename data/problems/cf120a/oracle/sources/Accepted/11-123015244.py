# import math
# tot = int(input())
# arr = list(map(int,input().split(" ")))
# p = tot - 1
# p = int(math.log(p)/math.log(2))
# k = range(1,2**p + 1)
# ct = 1
# prev = 0
# for i in range(tot -1):
#      print(prev + arr[i])
#      prev = arr[i] + prev
#      if(arr[i]!=0):
#           p = int(math.log(tot - 1 - i)/math.log(2))
#           arr[i + 2 ** p] += arr[i]

# print(tp)
# for i in range(1,tot):
#      print(tp)

# for i in k:
#      print(sum(arr[:i]))
# for i in range(2**p + 1,tot):
#      print(sum(arr[:i]) + sum(arr[:ct]))
#      ct += 1
# a = input()
# lst = []
# for i in a:
#      if(i=='<'):
#           sl = []
#           sl.append("<")
#      else:
#           sl.append(i)
#           if i=='>':
#                lst.append(sl)
# sp = 0
# li = 0
# for i in lst:
#      if li!=0:
#           if lst[li][1] !='/' and lst[li-1][1] != "/":
#                sp += 1
#      for x in range(2 * sp):
#           print(" ",end='')
#      for x in i:
#           print(x,end="")
#      print()
     
#      if li<len(lst) - 1:
#           if lst[li][1] =='/' and lst[li+1][1] == "/":
#                sp -= 1
#      li += 1
# a = input()
# b = int(input())
with open('input.txt','r') as inp:
     lines = inp.readlines()
a = lines[0]#[:len(lines[0] - 2)]
a = a[0:len(lines[0]) - 1]
# print(len(lines[0]))
b= int(lines[1][:1])
# print(a,b)
# exit()
op = 'e'
if a == "front":
     if b == 1:
          op = 'L'
          # print("L")
     else:
          op = 'R'
          # print("R")
else:
     if b == 2:
          op = 'L'
          # print("L")
     else:
          op = 'R'
with open('output.txt','w') as inp:
     inp.write(op)
          # print("R")
# print(ct)