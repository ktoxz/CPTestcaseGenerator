tst = int(input())

vals = []
cost = 500000
vals2 = []

for i in range(0,tst):
  arr = [int(x) for x in input().split()]
  vals.append(arr)

count = 0
ind = 0

for lst in vals:
  arr = []
  arr.append(lst[0])
  arr.append(lst[1])
  arr.append(lst[2])
  vals2.append(arr)

stop = False

for lst in vals:
  count += 1
  stop = False
  for i in vals2:
    if lst[0] < i[0] and lst[1] < i[1] and lst[2] < i[2]:
      stop = True
  if stop == False:
    if lst[3] < cost:
      cost = lst[3]
      ind = count

print(ind)