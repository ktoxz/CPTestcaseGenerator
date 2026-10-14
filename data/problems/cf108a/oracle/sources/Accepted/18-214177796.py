a,b=map(str,input().split(':'))
if a[0]=='0':
  list(a).remove(a[0])
if b[0]=='0':
  list(b).remove(b[0])
a=int(a)
b=int(b)
if a==23 and b>=32:
    print('00:00')
elif (a==0 and b<=59)or(a==1 and b<=9):
    print('01:10')
elif (a==1 and b>=10)or(a==2 and b<=19):
    print('02:20')
elif (a==2 and b>=20)or(a==3 and b<=29):
    print('03:30')
elif (a==3 and b>=30)or(a==4 and b<=39):
    print('04:40')
elif (a==4 and b>=40)or(a==5 and b<=49):
    print('05:50')
elif (a==5 and b>=50)or(6<=a<=9 and b<=59)or(a==10 and b==1):
    print('10:01')
elif (a==10 and b>=1)or(a==11 and b<=10):
    print('11:11')
elif (a==11 and b>=11)or(a==12 and b<=20):
    print('12:21')
elif (a==12 and b>=21)or(a==13 and b<=30):
    print('13:31')
elif (a==13 and b>=31)or(a==14 and b<=40):
    print('14:41')
elif (a==14 and b>=41)or(a==15 and b<=50):
    print('15:51')
elif (a==15 and b>=51)or(16<=a<=19 and b<=59)or(a==20 and b==2):
    print('20:02')
elif (a==20 and b>=2)or(a==21 and b<=11):
    print('21:12')
elif (a==21 and b>=12)or(a==22 and b<=21):
    print('22:22')
else:
    print('23:32')