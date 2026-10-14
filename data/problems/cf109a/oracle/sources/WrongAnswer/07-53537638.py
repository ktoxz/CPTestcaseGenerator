import math
n = int(input())

a = 1
b = 1

a_inc_list = list()
b_inc_list = list()
b_flag = True
a_flag = True

while(1):
    a = ((n-(b*7))/4)
    a = math.floor(a)
    if (a*4+b*7) == n:
        for i in range(a):
            b_inc_list.append(4)
        for i in range(b):
            b_inc_list.append(7)
        break

    elif (a*4+b*7 < n):
        b += 1

    elif((a*4)+(b*7) > n):
        a_flag = False
        break

a, b = 1, 1

while(1):
    b = (n-(a*4))/7
    b = math.floor(b)

    if (a*4+b*7 < n):
        a += 1
    elif (a*4+b*7) == n:
        for i in range(a):
            a_inc_list.append(4)
        for i in range(int(b)):
            a_inc_list.append(7)
        break

    elif((a*4)+(b*7) > n):
        b_flag = False
        break


if(a_flag == True and b_flag == True):
    if(len(a_inc_list) < len(b_inc_list)):
        for i in a_inc_list:
            print(i, end='')
    else:
        for i in b_inc_list:
            print(i, end='')

else:
    if(a_flag):
        for i in a_inc_list:
            print(i, end='')
    if(b_flag):
        for i in b_inc_list:
            print(i, end='')