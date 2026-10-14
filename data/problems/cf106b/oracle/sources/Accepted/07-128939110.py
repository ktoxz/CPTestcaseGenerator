#106B (86No. Problem B)
n = int(input())
des = []
for i in range(n):
  t = list(map(int,input().split()))
  des.append(t)  

price = 1001
for i in range(n):
  flag = 0
  for j in range(n):
    if des[i][0] < des[j][0] and des[i][1] < des[j][1] and des[i][2] < des[j][2]:
      flag = 1
      break
  if (flag == 0  and des[i][3] < price):
    res = i+1
    price = des[i][3]
    # print(price)
print(res)