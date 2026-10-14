a, b = map(int, input().split(':'))
if 5 < a < 10:
    print('10:01')
elif 15 < a < 20:
    print('20:02')
elif 0 < a < 6:
    if b < 10*a:
        print('0' + str(a) + ':' + str(10*a))
    elif b > 10*a and a != 15:
        print('0' + str(a+1) + ':' + str(10*(a+1)))
    elif b > 10*a and a == 5:
        print('10:01')
elif 10 < a < 16:
    if b < (a//10)*10 + a%10:
        print(str(a) + ':' + str(a%10) + str(a//10))
    elif b > (a//10)*10 + a%10 and a != 15 :
        print(str(a+1) + ':' + str((a+1)%10) + str(a//10))
    elif b > (a//10)*10 + a%10 and a == 15 :
        print('20:02')
else:
    if 20 < a < 24 and b < (a//10)*10 + a%10:
        print(str(a) + ':' + str(a%10) + str(a//10))
    elif 20 < a < 23 and b > (a//10)*10 + a%10:
        print(str(a+1) + ':' + str((a+1)%10) + str(a//10))
    elif a == 23 and b > (a//10)*10 + a%10:
        print('00:00')