num=int(input())
one_digit=False
times=0

def check(x,times,one_digit):
  x_string=str(x)
  x_list=[]
  total=0
  for i in x_string:
    x_list.append(i)
  for i in range(len(x_list)):
    total+=int(x_list[i])
  times+=1
  x=total
  if total<=9:
    one_digit=True
  return x,times,one_digit
  
  
while one_digit==False:
  num,times,one_digit = check(num,times,one_digit)
  

print(times)